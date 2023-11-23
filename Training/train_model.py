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
    ("Expert in Linux kernel and system administration", {"entities": [(5, 10, "SKILL"), (17, 26, "SKILL"), (33, 53, "SKILL")]}),
    ("Advanced networking skills - configuring routers, switches, firewalls", {"entities": [(8, 22, "SKILL"), (25, 41, "SKILL"), (44, 54, "SKILL"), (57, 66, "SKILL")]}), 
    ("Experience setting up Kubernetes clusters on AWS and GCP", {"entities": [(17, 28, "SKILL"), (37, 57, "SKILL"), (61, 64, "SKILL")]}),
    ("Skilled software developer with 5 years building scalable web apps", {"entities": [(10, 26, "SKILL"), (52, 68, "SKILL"), (73, 83, "SKILL")]}),
    ("Proficiency in Java, Python, C++, JavaScript, and Golang", {"entities": [(14, 19, "SKILL"), (22, 28, "SKILL"), (31, 34, "SKILL"), (37, 47, "SKILL"), (52, 58, "SKILL")]}),
    ("Expertise in full stack development using MongoDB, Express, React, Node", {"entities": [(20, 33, "SKILL"), (44, 51, "SKILL"), (55, 61, "SKILL"), (65, 70, "SKILL"), (74, 78, "SKILL")]}),
    ("Experience with machine learning libraries PyTorch, TensorFlow, Keras", {"entities": [(17, 45, "SKILL"), (50, 60, "SKILL"), (65, 75, "SKILL"), (80, 85, "SKILL")]}),
    ("Skilled in CI/CD pipelines, GitLab, Jenkins, Bamboo, CircleCI", {"entities": [[10, 24, "SKILL"], [29, 35, "SKILL"], [40, 47, "SKILL"], [52, 59, "SKILL"], [64, 72, "SKILL"]]}),
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
    ("Linux operating system", {"entities": [(0, 5, "SKILL")]}),
    ("Windows Server administration", {"entities": [(0, 6, "SKILL"), (17, 28, "SKILL")]}),
    ("Network configuration and troubleshooting", {"entities": [(0, 8, "SKILL"), (25, 42, "SKILL")]}),
    ("TCP/IP, OSI model", {"entities": [(0, 7, "SKILL"), (12, 17, "SKILL")]}), 
    ("Routing protocols like OSPF, BGP", {"entities": [(0, 15, "SKILL"), (22, 25, "SKILL"), (30, 33, "SKILL")]}),
    ("Cisco switching and routing", {"entities": [(0, 5, "SKILL"), (13, 19, "SKILL")]}),
    ("VPN configuration", {"entities": [(0, 13, "SKILL")]}),
    ("Firewall administration", {"entities": [(0, 9, "SKILL"), (17, 28, "SKILL")]}),
    ("Network security", {"entities": [(0, 14, "SKILL")]}),
    ("Penetration testing", {"entities": [(0, 19, "SKILL")]}),
    ("Burp Suite", {"entities": [(0, 9, "SKILL")]}),
    ("Wireshark network analysis", {"entities": [(0, 9, "SKILL"), (17, 32, "SKILL")]}),
    ("CCNA certification", {"entities": [(0, 10, "SKILL")]}), 
    ("VMware administration", {"entities": [(0, 6, "SKILL"), (17, 28, "SKILL")]}),
    ("SAN storage configuration", {"entities": [(0, 3, "SKILL"), (14, 32, "SKILL")]}),
    ("NAS storage administration", {"entities": [(0, 3, "SKILL"), (15, 33, "SKILL")]}),
    ("RAID arrays", {"entities": [(0, 7, "SKILL")]}),
    ("Docker containerization", {"entities": [(0, 6, "SKILL"), (17, 32, "SKILL")]}),
    ("Kubernetes", {"entities": [(0, 10, "SKILL")]}),
    ("Jenkins CI/CD pipelines", {"entities": [(0, 7, "SKILL"), (17, 30, "SKILL")]}), 
    ("Ansible automation", {"entities": [(0, 6, "SKILL"), (17, 27, "SKILL")]}),
    ("Terraform infrastructure-as-code", {"entities": [(0, 9, "SKILL"), (18, 38, "SKILL")]}),
    ("Azure administration", {"entities": [(0, 6, "SKILL"), (17, 29, "SKILL")]}),
    ("AWS cloud architecture", {"entities": [(0, 3, "SKILL"), (13, 29, "SKILL")]}),
    ("Google Cloud Platform", {"entities": [(0, 22, "SKILL")]}),
    ("DevOps culture and practices ", {"entities": [(0, 6, "SKILL"), (18, 34, "SKILL")]}),
    ("Agile development methodologies", {"entities": [(0, 5, "SKILL"), (20, 42, "SKILL")]}),
    ("Waterfall SDLC", {"entities": [(0, 8, "SKILL"), (13, 16, "SKILL")]}),
    ("Object-oriented analysis and design", {"entities": [(0, 25, "SKILL"), (31, 36, "SKILL")]}), 
    ("SQL database programming", {"entities": [(0, 3, "SKILL"), (14, 28, "SKILL")]}),
    ("Oracle database administration", {"entities": [(0, 6, "SKILL"), (17, 35, "SKILL")]}),
    ("MongoDB NoSQL databases", {"entities": [(0, 7, "SKILL"), (15, 29, "SKILL")]}),
    ("Redis in-memory caching", {"entities": [(0, 5, "SKILL"), (17, 29, "SKILL")]}),
    ("Data modeling and warehousing", {"entities": [(0, 15, "SKILL"), (21, 32, "SKILL")]}), 
    ("ETL processing pipelines", {"entities": [(0, 3, "SKILL"), (15, 31, "SKILL")]}),
    ("Hadoop cluster configuration", {"entities": [(0, 6, "SKILL"), (20, 38, "SKILL")]}),
    ("Spark big data processing", {"entities": [(0, 5, "SKILL"), (16, 30, "SKILL")]}),
    ("Tableau data visualization", {"entities": [(0, 7, "SKILL"), (17, 33, "SKILL")]}), 
    ("Power BI business analytics", {"entities": [(0, 8, "SKILL"), (17, 33, "SKILL")]}),
    ("Python programming", {"entities": [(0, 6, "SKILL"), (17, 28, "SKILL")]}), 
    ("Java Spring Boot framework", {"entities": [(0, 4, "SKILL"), (10, 26, "SKILL")]}),  
    ("PHP web application development", {"entities": [(0, 3, "SKILL"), (14, 37, "SKILL")]}),
    ("Ruby on Rails web framework", {"entities": [(0, 3, "SKILL"), (10, 27, "SKILL")]}),
    ("JavaScript front-end development", {"entities": [(0, 10, "SKILL"), (22, 40, "SKILL")]}),
    ("React web applications", {"entities": [(0, 5, "SKILL"), (16, 30, "SKILL")]}),
    ("Angular single page applications", {"entities": [(0, 7, "SKILL"), (17, 37, "SKILL")]}),
    ("Node.js back-end services", {"entities": [(0, 7, "SKILL"), (17, 29, "SKILL")]}),
    ("REST API design and development", {"entities": [(0, 10, "SKILL"), (28, 47, "SKILL")]}),
    ("GraphQL API development", {"entities": [(0, 7, "SKILL"), (17, 31, "SKILL")]}),
    ("Unit testing frameworks like JUnit", {"entities": [(0, 15, "SKILL"), (24, 29, "SKILL")]}),
    ("UX design and usability", {"entities": [(0, 7, "SKILL"), (16, 27, "SKILL")]}),
    ("Git version control system", {"entities": [(0, 18, "SKILL"), (30, 36, "SKILL")]}),
    ("Continuous integration and delivery", {"entities": [(0, 28, "SKILL"), (36, 44, "SKILL")]}), 
    ("R language data analysis", {"entities": [(0, 11, "SKILL"), (20, 33, "SKILL")]}), 
    ("MATLAB numerical computing", {"entities": [(0, 6, "SKILL"), (17, 31, "SKILL")]}),
    ("C++ high performance programming", {"entities": [(0, 2, "SKILL"), (18, 37, "SKILL")]}),
    ("Multithreading and concurrency", {"entities": [(0, 15, "SKILL"), (22, 34, "SKILL")]}),
    ("Cryptography and encryption algorithms", {"entities": [(0, 13, "SKILL"), (24, 44, "SKILL")]}),
    ("Cybersecurity awareness ", {"entities": [(0, 14, "SKILL"), (26, 40, "SKILL")]}),
    ("Penetration testing and ethical hacking", {"entities": [(0, 23, "SKILL"), (31, 47, "SKILL")]}),
    ("Artificial intelligence and machine learning", {"entities": [(0, 25, "SKILL"), (35, 52, "SKILL")]}),
    ("Neural networks and deep learning", {"entities": [(0, 15, "SKILL"), (25, 39, "SKILL")]}), 
    ("Computer vision with OpenCV", {"entities": [(0, 16, "SKILL"), (26, 32, "SKILL")]}),
    ("Natural language processing techniques", {"entities": [(0, 33, "SKILL"), (46, 58, "SKILL")]}),
    ("Recommender systems algorithms", {"entities": [(0, 23, "SKILL"), (30, 42, "SKILL")]}),
    ("Python", {"entities": [(0, 6, "SKILL")]}),
    ("Java", {"entities": [(0, 4, "SKILL")]}),
    ("JavaScript", {"entities": [(0, 10, "SKILL")]}),
    ("TypeScript", {"entities": [(0, 10, "SKILL")]}),
    ("C++", {"entities": [(0, 3, "SKILL")]}),
    ("C#", {"entities": [(0, 2, "SKILL")]}),
    ("Go", {"entities": [(0, 2, "SKILL")]}),
    ("Ruby", {"entities": [(0, 4, "SKILL")]}),
    ("PHP", {"entities": [(0, 3, "SKILL")]}),
    ("Swift", {"entities": [(0, 5, "SKILL")]}),
    ("Rust", {"entities": [(0, 4, "SKILL")]}),
    ("Dart", {"entities": [(0, 4, "SKILL")]}),
    ("Kotlin", {"entities": [(0, 6, "SKILL")]}),
    ("SQL", {"entities": [(0, 3, "SKILL")]}),
    ("NoSQL", {"entities": [(0, 5, "SKILL")]}),
    ("C", {"entities": [(0, 1, "SKILL")]}),
    ("Scala", {"entities": [(0, 5, "SKILL")]}),
    ("Perl", {"entities": [(0, 4, "SKILL")]}),
    ("Haskell", {"entities": [(0, 7, "SKILL")]}),
    ("Bash", {"entities": [(0, 4, "SKILL")]}),
    ("Shell", {"entities": [(0, 5, "SKILL")]}),
    ("Cobol", {"entities": [(0,5, "SKILL")]}),
    ("Fortran", {"entities": [(0,7, "SKILL")]}),
    ("Visual Basic", {"entities": [(0,13, "SKILL")]}),
    ("Assembly", {"entities": [(0,9, "SKILL")]}),
    ("Pascal", {"entities": [(0,6, "SKILL")]}),
    ("Ada", {"entities": [(0,3, "SKILL")]}),
    ("ABAP", {"entities": [(0,4, "SKILL")]}), 
    ("RPG", {"entities": [(0,3, "SKILL")]}),
    ("Lisp", {"entities": [(0,4, "SKILL")]}),
    ("Prolog", {"entities": [(0,6, "SKILL")]}),
    ("F#", {"entities": [(0,2, "SKILL")]}),
    ("Lua", {"entities": [(0,3, "SKILL")]}),
    ("MATLAB", {"entities": [(0,6, "SKILL")]}),
    ("SAS", {"entities": [(0,3, "SKILL")]}),
    ("SPSS", {"entities": [(0,4, "SKILL")]}),
    ("R", {"entities": [(0,1, "SKILL")]}),
    ("Julia", {"entities": [(0,5, "SKILL")]}),
    ("Mahout", {"entities": [(0,6, "SKILL")]}), 
    ("Solr", {"entities": [(0,4, "SKILL")]}),
    ("Lucene", {"entities": [(0,6, "SKILL")]}),
    ("HBase", {"entities": [(0,4, "SKILL")]}),
    ("Cassandra", {"entities": [(0,9, "SKILL")]}), 
    ("Neo4j", {"entities": [(0,5, "SKILL")]}),
    ("Unix", {"entities": [(0,4, "SKILL")]}),
    ("Linux", {"entities": [(0,5, "SKILL")]}),
    ("Windows", {"entities": [(0,7, "SKILL")]}),
    ("MacOS", {"entities": [(0,5, "SKILL")]}),
    ("Android", {"entities": [(0,7, "SKILL")]}),
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
output_dir = "TrainedModel/test"  # Replace with your desired output directory
trained_nlp_skills_updated.to_disk(output_dir)
print("Model saved to:", output_dir)
