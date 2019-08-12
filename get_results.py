#
# MTURK IMAGE ANNOTATION TOOL
#

# Return results for a specific HIT.

import sys
import xmltodict

import mturk

hit_id = sys.argv[1]
worker_results = mturk.client.list_assignments_for_hit(
    HITId=hit_id,
    AssignmentStatuses=['Submitted']
)

if worker_results['NumResults'] > 0:
    for assignment in worker_results['Assignments']:
        xml_doc = xmltodict.parse(assignment['Answer'])

        print("Worker's answer was:")
        if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
            # Multiple fields in HIT layout
            for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
                print("For input field: " + answer_field['QuestionIdentifier'])
                print("Submitted answer: " + answer_field['FreeText'])
        else:
            # One field found in HIT layout
            print("For input field: " +
                  xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
            print("Submitted answer: " +
                  xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
else:
    print("No results ready yet")
