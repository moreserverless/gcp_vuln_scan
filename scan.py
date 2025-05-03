import json
from typing import List

from google.oauth2.service_account import Credentials
from google.cloud.devtools import containeranalysis_v1

from grafeas.grafeas_v1 import types
from grafeas.grafeas_v1 import Severity

import functions_framework


def get_vulnerabilities():
    """
    For every image in a project's artifact repository obtain the vulnerabilities.  
    If the vulnerability's SEVERITY is MEDIUM, HIGH or CRITICAL add it to the 
    list to be reported.

    INPUTS:
    NONE

    RETURN:
    all_vuln : a list of all MEDIUM, HIGH and CRITICAL vulnerabilites for every
                image in a project's artifact repository
    """
    # Set the project which contains the artifact repository to scan
    #
    # Possible improvement: What ever invokes this cloud run function
    # could pass in the project id which would eliminate the need to
    # hardcode it.
    project_id = f'projects/<PROJECT_ID>'

    all_vuln = []

    grafeas_client = client.get_grafeas_client()
    filter_str = 'kind="VULNERABILITY"'
    vulnerabilities = grafeas_client.list_occurrences(parent=project_id, filter=filter_str)

    for v in vulnerabilities:
        if v.vulnerability.effective_severity == Severity.MEDIUM 
            or v.vulnerability.effective_severity == Severity.HIGH 
            or v.vulnerability.effective_severity == Severity.CRITICAL :
            all_vuln.append(v)

    return all_vuln

def parse_vulnerabilities(vulns):
    """
    Given a list of vulnerabilities, maps MEDIUM, HIGH and CRITICAL vulnerabilities
    to each image in a project's artifact repository.

    INPUTS
    :vulns: A list of MEDIUM, HIGH, and CRITICAL vulnerabilites for ALL images in a project's
            artifact repository.  

    RETURNS:
    NONE

    """

    # map the vulnerabilities to project.image_name and based on severity
    vuln_dict = {}

    # keep track if the CVE has already been seen. The same CVE can show up multiple
    # times within an image.  If it hasn't been seen, add it otherwise skip.
    cve_seen = []
    for v in vulns:
        name_parts = v.name.split("/")
        project_name = name_parts[1]

        if project_name not in vuln_dict:
            vuln_dict[project_name] = {}

        # URI is returned in the following format:
        # https://REGION-docker.pkg.dev/PROJECT_ID/REPO_NAME/IMAGE_NAME@sha256:some_sha_hash_value"
        # split it on the '@' symbol and then on the forward slash, '/', symbol
        # The name of the image will be the last element after splitting on the forward slash
        resource_uri_part_1 = v.resource_uri.split("@")
        resource_uri_part_2 = resource_uri_part_1[0].split("/")
        image_name = resource_uri_part_2[len(resource_uri_part_2) - 1]

        # See README.md for an example of the dictionary format
        if image_name not in vuln_dict[project_name]:
            vuln_dict[project_name][image_name] = {
                "med": [],
                "high": [],
                "critical": [] }
        
        if 'vulnerability' in v:
            vuln_info = {
                "affected_package": "",
                "affected_version": "",
                "fixed_package": "",
                "fixed_version": "",
                "cve_description": "",
                "package_type": ""
            }
            
            package_issue = v.vulnerability.package_issue[0]

            # the same CVE can show up multiple times but we only need to
            # see it once.  Skip if it has already been seen and logged
            if 'short_description' in v.vulnerability:
                cve_description = v.vulnerability.short_description
                if cve_description in cve_seen:
                    continue
                else:
                    cve_seen.append(cve_description)
                    vuln_info["cve_description"] = cve_description

            vuln_info["affected_package"] = package_issue.affected_package
            vuln_info["affected_version"] = package_issue.affected_version.full_name
            vuln_info["package_type"] = package_issue.package_type

            if 'fixed_package' in package_issue:
                vuln_info["fixed_package"] = package_issue.fixed_package
                vuln_info["fixed_version"] = package_issue.fixed_version.full_name

            if v.vulnerability.effective_severity == Severity.MEDIUM:
                vuln_dict[project_name][image_name]["med"].append(vuln_info)
            elif v.vulnerability.effective_severity == Severity.HIGH:
                vuln_dict[project_name][image_name]["high"].append(vuln_info)
            elif v.vulnerability.effective_severity == Severity.CRITICAL:
                vuln_dict[project_name][image_name]["critical"].append(vuln_info)

    return vuln_dict