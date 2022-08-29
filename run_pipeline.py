# -*- coding: utf-8 -*-

from abulafia.actions import Forward, Aggregate, SeparateBBoxes
from abulafia.task_specs import ImageSegmentation, TaskSequence, MulticlassVerification, \
    ImageClassification, FixImageSegmentation, SegmentationClassification, AddOutlines, \
    LabelledSegmentationVerification, SegmentationVerification
import argparse
import json
import toloka.client as toloka


# Set up the argument parser
ap = argparse.ArgumentParser()

# Add argument for input
ap.add_argument("-c", "--creds", required=True,
                help="Path to a JSON file that contains Toloka credentials. "
                     "The file should have two keys: 'token' and 'mode'. "
                     "The key 'token' should contain the Toloka API key, whereas "
                     "the key 'mode' should have the value 'PRODUCTION' or 'SANDBOX' "
                     "that defines the environment in which the pipeline should be run.")

# Parse the arguments
args = vars(ap.parse_args())

# Assign arguments to variables
cred_file = args['creds']

# Read the credentials from the JSON file
with open(cred_file) as cred_f:

    creds = json.loads(cred_f.read())
    tclient = toloka.TolokaClient(creds['token'], creds['mode'])

# Create training and examination pools
detect_text_exam = ImageClassification(configuration="config/00_detect_text_exam.yaml", client=tclient)
verify_outlines_exam = MulticlassVerification(configuration="config/00_verify_outlines_exam.yaml", client=tclient)
detect_target_exam = SegmentationVerification(configuration="config/00_detect_target_exam.yaml", client=tclient)
verify_target_exam = LabelledSegmentationVerification(configuration="config/00_verify_target_exam.yaml", client=tclient)

# Create tasks and actions
detect_text = ImageClassification(configuration="config/01_detect_text.yaml",
                                  client=tclient)
outline_text = ImageSegmentation(configuration="config/02_outline_text.yaml",
                                 client=tclient)
forward_detect = Forward(configuration="config/03_forward_detect.yaml",
                         client=tclient, targets=[outline_text])
aggregate_detect = Aggregate(configuration="config/04_aggregate_detect.yaml",
                             task=detect_text, forward=forward_detect)
verify_outlines = MulticlassVerification(configuration="config/05_verify_outlines.yaml",
                                         client=tclient)
fix_outlines = FixImageSegmentation(configuration="config/06_fix_outlines.yaml",
                                    client=tclient)
has_target = SegmentationClassification(configuration="config/07_detect_target.yaml",
                                        client=tclient)
separate_bboxes = SeparateBBoxes(configuration="config/08_separate_bboxes.yaml",
                                 target=has_target)
forward_verify = Forward(configuration="config/09_forward_verify.yaml", client=tclient,
                         targets=[fix_outlines, separate_bboxes])
aggregate_verify = Aggregate(configuration="config/10_aggregate_verify.yaml",
                             task=verify_outlines, forward=forward_verify)
outline_targets = AddOutlines(configuration="config/11_outline_target.yaml",
                              client=tclient)
forward_targets = Forward(configuration="config/12_forward_target.yaml",
                          client=tclient, targets=[outline_targets])
aggregate_targets = Aggregate(configuration="config/13_aggregate_target.yaml",
                              task=has_target, forward=forward_targets)
verify_target = LabelledSegmentationVerification(configuration="config/14_verify_target.yaml",
                                                 client=tclient)
forward_verify_target = Forward(configuration="config/15_forward_verify_target.yaml",
                                client=tclient, targets=[])
aggregate_verify_target = Aggregate(configuration="config/16_aggregate_verify_target.yaml",
                                    task=verify_target, forward=forward_verify_target)

# Create a task sequence
pipe = TaskSequence(sequence=[detect_text_exam,
                              verify_outlines_exam,
                              detect_target_exam,
                              verify_target_exam,
                              detect_text,
                              aggregate_detect,
                              forward_detect,
                              outline_text,
                              verify_outlines,
                              aggregate_verify,
                              forward_verify,
                              fix_outlines,
                              separate_bboxes,
                              has_target,
                              aggregate_targets,
                              forward_targets,
                              outline_targets,
                              verify_target,
                              aggregate_verify_target,
                              forward_verify_target],
                    client=tclient)

# Start the task sequence
pipe.start()
