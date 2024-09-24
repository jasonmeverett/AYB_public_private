from crewai_tools import BaseTool


_case_summary_cache = {
        "1064638": """Case Intent: The primary objective of this support case was to resolve the customer's issue with the "Redact Sensitive Data" toggle, which was not turning off, preventing the customer from viewing unredacted logs necessary to understand autoscaling patterns of the CML CPU Cluster (workspace instances).

Effective Actions:

    The support team attached screenshots of the redaction settings and the session kinit file to the case for reference.
    They confirmed the customer's data was being sent to Observability for multiple environments.
    They explained the function of the "Redact Sensitive Data" option and the nature of the redacted log lines.
    The support team identified that the customer's issue was with the inability to disable the redaction feature, not with the redaction process itself.

Effective Solutions:

    The support team provided clarification on how to generate a log bundle without selecting the "Redact sensitive information" option.
    The exact configuration change that resolved the issue:
        Instructed the customer to navigate to Site Administration > Support and use the "Generate Diagnostic Bundle" button to toggle the redaction option off.
    The customer successfully generated the logs without redaction based on this guidance.

Pending Issues and Recommendations:

    There are no pending issues related to the log redaction case as it was resolved.
    For further discussion on autoscaling patterns, the customer was directed to continue on case 1064329.

Customer Sentiment:

    The customer expressed dissatisfaction initially due to the inability to turn off the redaction toggle.
    Satisfaction was implied once the issue was resolved and unredacted logs were obtained.

Technical Complexity:

    The technical difficulty of the case is rated as 2 out of 10.
    The challenge was mainly in identifying that the customer's issue was with the interface's functionality (toggle button) rather than the redaction process itself.
""",
        "1063676": """Case Intent: The main objective of the support case was to resolve the issue where users were unable to transfer (scp) files from a high compute cluster (HPC) to a Cloudera Machine Learning (CML) project session, despite having valid permissions.

Effective Actions:

    The support team requested and reviewed the log of the failed scp attempt (scp_output.txt).
    The issue was discussed with Cloudera's Cloud engineering team for their input.

Effective Solutions:

    The case did not result in a specific solution from Cloudera's side as it was determined that the problem likely did not originate from Cloudera software.
    No exact configuration changes or values were provided as part of the resolution because the investigation suggested that the issue was external to Cloudera's service.

Pending Issues and Recommendations:

    The support team recommended that the customer review the issue with the AWS team and their internal IT team.
    There is an open recommendation to reopen the case with Cloudera if, after reviewing with AWS and the internal team, the customer still suspects the issue to be with CML.

Customer Sentiment:

    The customer's sentiment is not explicitly mentioned, but there might be a sense of unresolved concern since the case was closed without a technical resolution from Cloudera.

Technical Complexity:

    The technical difficulty of this case is rated as 5 out of 10.
    The specific technical challenge was the determination of the root cause of the scp issue, given that it involved multiple environments (HPC, CML, local PC) and potential network or permission configurations.
""",
        "1060330": """Case Intent: The primary objective of the case was to resolve the issue of the Datalake (DL) cluster nodes failing due to a certificate issue, which led to the DL being in a defunct state.

Effective Actions:

    The support team identified that the DL's private certificates were about to expire, causing health alerts.
    An IDBroker node was out of sync with the Cloudera Manager server, preventing certificate rotations.
    The team attempted a 'Repair' on the IDBroker node and found that the attached PostgreSQL Database server was not being detected by Cloudbreak due to recent restoration efforts.
    A restart sequence was planned for the Data Lake and attached Data Hub, which included stopping and starting these services in a specific order.
    The support team manually started instances and restarted agents when the Cloudera Manager UI was inaccessible.
    They also used a script to start Knox and planned to renew the Data Lake host certificates using another script.

Effective Solutions:

    The team successfully renewed the Data Lake host certificates using a script (CDP_CM_AUTOTLS_ROTATE.sh) due to the unhealthy state of the cluster.
    This allowed for access to the UI and both nodes returned to a healthy state.
    The Data Hub cluster certificates were renewed from the CDP console.

Pending Issues and Recommendations:

    The RDBMS status in Cloudbreak was incorrect, showing as "Terminated" despite the database being active. This required an engineering escalation to update entries in the backend CB database.
    The engineering team ultimately suggested creating a new Data Lake and performing a backup and restore on it, as updating the backend database was not possible.

Customer Sentiment: The customer's sentiment seemed to fluctuate throughout the case. There were expressions of urgency and importance due to production environment impact. However, there was no explicit mention of satisfaction or dissatisfaction at the conclusion of the case.

Technical Complexity: The case's technical difficulty is rated at 8 out of 10. The specific technical challenges included:

    Dealing with certificate expirations and renewals in an unhealthy cluster state.
    Restoring a PostgreSQL Database server that was not being detected by Cloudbreak.
    Troubleshooting issues with the Cloudera Manager UI accessibility and service status.
    Coordinating with engineering teams to address backend database inconsistencies.
""",
    "1060986": """Case Intent: The main objective of the support case was to resolve the issue of being unable to open a CML session with a GPU after changing the GPU instance type from g4dn.xlarge to g4dn.2xlarge in the CML workspace.

Effective Actions:

    The support team updated various environments related to Observability, including codep-pd-eng, codep-pd-datalake, codep-pd-datalake-default, catalyst, compute-1696047178-n9kr, and codex-prod-impala-dwx.

Effective Solutions:

    The root cause of the issue was identified and fixed by the support team. The exact configuration changes and values that led to the resolution were not provided in the comments.

Pending Issues and Recommendations:

    There are no pending issues mentioned, and no further action is needed as the case was resolved and could be closed according to the support team's comments.

Customer Sentiment:

    The customer sentiment is not explicitly stated in the comments; however, the quick identification and resolution of the issue may imply customer satisfaction.

Technical Complexity:

    The technical complexity of the case is rated as 5 out of 10, considering the need to identify and fix an issue related to GPU instance modifications within a CML workspace. The specific technical challenge encountered was to address the inability to open a session after changing the GPU instance type, which requires an understanding of the CML environment and GPU configurations.

In summary, the support case involved resolving an issue with creating a CML session with a GPU after an instance type change. The issue was promptly identified and resolved by the support team, with no further action needed and no pending issues. Customer sentiment was not directly mentioned but is anticipated to be positive given the outcome. The technical challenge was moderately complex, involving environment configurations and GPU instance specifications.
"""
    }

class CDXSummarizerTool(BaseTool):
    name: str = "CDXSummarizerTool"
    description: str = "Provides information on a case based on a case number"
    
    def _fetch_data(self, case_number: str):
        if case_number.startswith("#"):
            case_number = case_number[1:]

        if case_number in list(_case_summary_cache.keys()):
            return {
                "case_number": case_number,
                "summary": _case_summary_cache[case_number]
            }
        else:
            raise ValueError(f"Case number {case_number} is not in the case summary cache.")
        
        return r.json()

    def _run(self, case_number: str) -> str:
        with open('/tmp/crew.log', 'a') as tools_log:
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('...\n')
          tools_log.write('## Using the CXGenius Case Summarizer for this request.\n')
        if not isinstance(case_number, str):
            case_number = str(case_number)
        response = self._fetch_data(case_number)
        return response



if __name__ == "__main__":

    tool = CDXSummarizerTool()
    
    # This should work
    summary_out1 = tool._run("1060986")
    summary_out2 = tool._run("#1060986")
    summary_out3 = tool._run(1060986)
    assert summary_out1 == summary_out2 and summary_out2 == summary_out3
    print(summary_out1)


    # This should not work
    try:
        summary_out = tool._run("#1234567")
    except Exception as e:
        print(f"This call did not work, as expected! Error: {e}")
    

