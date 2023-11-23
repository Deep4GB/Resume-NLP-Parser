import spacy
from spacy.training.example import Example
import csv
import random

# Function to train the NER model with data from the CSV file and save it
def train_and_save_spacy_model(output_dir="TrainedModel/test2", iterations=20):
    nlp = spacy.blank("en")  # Create a blank 'en' model

    # Create a Named Entity Recognition (NER) pipeline
    ner = nlp.add_pipe("ner", name="ner", last=True)
    ner.add_label("SKILL")  # Add the label for skills recognition

    # Load skills data from CSV file and create training data
    TRAIN_DATA = []
    with open('data/newSkills.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            skill_text = row[0].strip()  # Skill text from the CSV row
            if skill_text:  # Check for non-empty skill text
                doc = nlp.make_doc(skill_text)
                entities = [(0, len(skill_text), "SKILL")]
                TRAIN_DATA.append((doc, {"entities": entities}))

    # Begin training
    nlp.begin_training()

    # Iterate through training data
    for itn in range(iterations):
        random.shuffle(TRAIN_DATA)
        losses = {}
        # Create examples and update the model
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(text, annotations)
            nlp.update([example], drop=0.5, losses=losses)

        print("Iteration:", itn+1, "Loss:", losses)

    # Save the trained model to the specified output directory
    nlp.to_disk(output_dir)
    print("Trained model saved to:", output_dir)
    return nlp

# Run the function to train the model using data from the CSV file only
trained_model = train_and_save_spacy_model()

# The trained_model variable now holds the trained SpaCy model
# You can use this model for NER tasks
