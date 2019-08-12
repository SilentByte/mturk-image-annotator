#
# MTURK IMAGE ANNOTATION TOOL
#

import os
import time
import boto3
import jinja2


region_name = 'us-east-1'
aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

sandbox_endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
production_endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=sandbox_endpoint_url,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def account_balance():
    return client.get_account_balance()['AvailableBalance']


def load_hit_template(**kwargs):
    loader = jinja2.FileSystemLoader(searchpath="./templates")
    environment = jinja2.Environment(loader=loader)
    template = environment.get_template('hit.jinja2')

    return template.render(**kwargs)


def dev_template_reload(image_url):
    while True:
        template_html = load_hit_template(
            image_url=image_url,
        )

        with open('hit_template.html', 'w') as fp:
            fp.write(template_html)

        print('Updated...')
        time.sleep(1)


def create_hit(image_url):
    template_html = load_hit_template(
        image_url=image_url,
    )

    template_xml = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
            <HTMLContent><![CDATA[{template_html}]]></HTMLContent>
            <FrameHeight>600</FrameHeight>
        </HTMLQuestion>""".strip()

    hit = client.create_hit(
        Title='Annotate the Values',
        Description='Please locate and annotate all values on the image according to the rules.',
        Keywords='text, quick, labeling',
        Reward='0.10',
        MaxAssignments=1,
        LifetimeInSeconds=172800,
        AssignmentDurationInSeconds=600,
        AutoApprovalDelayInSeconds=14400,
        Question=template_xml,
    )

    return hit['HIT']['HITId'], hit['HIT']['HITGroupId']
