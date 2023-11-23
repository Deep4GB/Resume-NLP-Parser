import spacy
import random
from spacy.training.example import Example

# Updated training data with phrases and skill-related keywords
UPDATED_TRAIN_DATA = [
    ("Proficient in Python, Java, and C++", {"entities": [(13, 19, "SKILL"), (21, 25, "SKILL"), (30, 33, "SKILL")]}),
    ("Experience with machine learning algorithms", {"entities": [(12, 28, "SKILL")]}),
    ("Familiar with TensorFlow and PyTorch", {"entities": [(13, 24, "SKILL"), (29, 36, "SKILL")]}),
    ("Strong understanding of HTML, CSS, and JavaScript", {"entities": [(19, 22, "SKILL"), (24, 27, "SKILL"), (32, 41, "SKILL")]}),
    ("Expertise in data analysis and visualization using Tableau", {"entities": [(20, 30, "SKILL"), (35, 46, "SKILL")]}),
    ("Skilled in SQL database management", {"entities": [(10, 13, "SKILL"), (24, 35, "SKILL")]}),
    ("Knowledge of React and Angular frameworks", {"entities": [(12, 17, "SKILL"), (22, 29, "SKILL")]}),
    ("Proficiency in MATLAB for numerical computing", {"entities": [(14, 19, "SKILL"), (28, 44, "SKILL")]}),
    ("Experience with cloud technologies like AWS and Azure", {"entities": [(17, 20, "SKILL"), (25, 30, "SKILL")]}),
    ("Expertise in natural language processing and NLP techniques", {"entities": [(20, 46, "SKILL"), (51, 54, "SKILL")]}),
    ("Familiarity with Git version control system", {"entities": [(16, 18, "SKILL"), (30, 36, "SKILL")]}),
    ("Knowledgeable in DevOps practices and CI/CD pipelines", {"entities": [(14, 20, "SKILL"), (37, 41, "SKILL")]}),
    ("Proficient in Java Spring and Hibernate frameworks", {"entities": [(14, 24, "SKILL"), (29, 38, "SKILL")]}),

    # Additional examples with skill-related keywords
    ("SQL", {"entities": [(0, 3, "SKILL")]}),
    ("JavaScript", {"entities": [(0, 10, "SKILL")]}),
    ("Machine Learning", {"entities": [(0, 16, "SKILL")]}),
    ("Data Analysis", {"entities": [(0, 13, "SKILL")]}),
    ("React.js", {"entities": [(0, 8, "SKILL")]}),
    ("AngularJS", {"entities": [(0, 9, "SKILL")]}),
    ("Node.js", {"entities": [(0, 7, "SKILL")]}),
    ("MongoDB", {"entities": [(0, 7, "SKILL")]}),
    ("AWS Cloud", {"entities": [(0, 8, "SKILL")]}),
    ("Azure Cloud", {"entities": [(0, 11, "SKILL")]}),
    ("Statistical Modeling", {"entities": [(0, 20, "SKILL")]}),
]

# Function to train the NER model with updated data
def train_spacy_ner_updated(data, iterations=20):
    nlp = spacy.blank("en")  # Create a blank 'en' model

    # Create a Named Entity Recognition (NER) pipeline
    ner = nlp.add_pipe("ner", name="ner", last=True)
    ner.add_label("SKILL")  # Add the label for skills recognition

    # Begin training
    nlp.begin_training()

    # Iterate through training data
    for itn in range(iterations):
        random.shuffle(data)
        losses = {}
        # Create examples and update the model
        for text, annotations in data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.5, losses=losses)

        print("Iteration:", itn+1, "Loss:", losses)

    return nlp

# Train the NER model with the updated data
trained_nlp_skills_updated = train_spacy_ner_updated(UPDATED_TRAIN_DATA)

# Test the trained model with a sample text
text_to_test = "Proficiency in Python and machine learning is required."
doc_test = trained_nlp_skills_updated(text_to_test)
for ent in doc_test.ents:
    if ent.label_ == "SKILL":
        print(f"Skill: {ent.text}")

# Save the trained model to disk
output_dir = "TrainedModel/skills"  # Replace with your desired output directory
trained_nlp_skills_updated.to_disk(output_dir)
print("Model saved to:", output_dir)
