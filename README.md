# Bloomtoon: AI Powered Plant Care Comics

**Bloomtoon** is a fun and helpful app designed to make plant care both educational and entertaining by providing personalized plant care tips through engaging comic strips. It combines the beauty of nature with creativity, making learning about plant care accessible, fun, and stress-free. Whether you're a beginner or a seasoned plant enthusiast, Bloomtoon offers something for everyone.

---

## **Project Overview**

### 🌿 **What is Bloomtoon?**
Bloomtoon is designed to help plant lovers of all levels take care of their plants in a fun, engaging way. It leverages the power of **comic storytelling** to simplify plant care, transforming otherwise complex care instructions into entertaining, easy-to-understand formats. With Bloomtoon, plant care becomes not only easy to understand but enjoyable to follow.

### 🌱 **Practical Application**
Bloomtoon is perfect for anyone who loves plants and wants to improve their plant care practices. Whether you’re just starting out or have years of gardening experience, Bloomtoon offers helpful advice in the form of visually stimulating and humorous comics. It’s the ideal bridge between plant science and entertainment.

---

## **Key Features**

### 🌸 **Case 1: Plant Care Comics**
- **Description:** Users upload a picture of their plant, and Bloomtoon generates a personalized care guide in the form of a comic strip.
- **Steps:**
  1. Users upload a picture of their plant.
  2. The app identifies the plant species and its care requirements.
  3. A comic strip is generated with care tips, including watering needs, sunlight exposure, and common plant issues.
  
### 🌿 **Case 2: Interactive Chatbot for Plant Help**
- **Description:** The interactive chatbot allows users to ask plant-related questions and receive illustrated answers in a comic format.
- **Steps:**
  1. Users type a plant care question (e.g., “Why are my leaves turning yellow?”).
  2. The chatbot retrieves the relevant answer and responds with a comic-style visual explanation.
  3. Users can explore more related topics or save answers for future reference.
  
### 🌾 **Case 3: RAG-Based FAQ System**
- **Description:** The app provides users with reliable, fact-based plant care answers via a Retrieval-Augmented Generation (RAG) system.
- **Steps:**
  1. Users browse or search for common plant care questions.
  2. The app fetches accurate answers using its RAG system, offering insightful plant care guidance.

### 🍃 **Case 4: Plant Vitals via Raspberry Pi (Side Project)**
- **Description:** Users can monitor real-time plant health by setting up a Raspberry Pi to gather data on plant vitals, such as soil moisture, temperature, and light exposure.
- **Steps:**
  1. Users connect a Raspberry Pi with sensors to monitor their plant's vitals.
  2. The app receives data from the Raspberry Pi and displays it in a comic-based format, offering insights into the plant's health.

---

## **Technologies Used**

- **Image Recognition:** For identifying plant species from photos.
- **Comic Generation:** Leveraging AI-driven text-to-image models (e.g., DALL·E, Stable Diffusion).
- **Chatbot Integration:** For dynamic, illustrated plant care Q&A using language models (e.g., GPT-4).
- **RAG System:** For retrieving plant care information from a knowledge database.
- **Raspberry Pi Integration:** For monitoring and displaying real-time plant vitals such as soil moisture, temperature, and light levels.
- **Frontend:** Streamlit for building a user-friendly web application interface.
- **Backend:** Python for data processing and model training, with potential use of MongoDB or Weaviate for storing plant care knowledge.
- **Version Control:** Git and GitHub for version control and collaboration.

---

## **Team P.L.A.N.T.S.**

### 🌿 **Team Overview**
We are **P.L.A.N.T.S.**—a team of passionate data scientists, and creators who, with this project, aim to bridge the gap between nature and technology. Together, we’re developing Bloomtoon to make plant care fun, informative, and accessible to everyone.

## 🌱 **Team Roles**

| Name                  | Primary Role               | Secondary Role                     |
|-----------------------|----------------------------|------------------------------------|
| **Stephen Oke**       | FrontEnd Dev                        | TBD                                |
| **Ibrahim Faruquee**  | TBD                        | TBD                                |
| **Lu Yao**            | Model Dev                        | TBD                                |
| **Keira James**       | TBD                        | TBD                                |


### 🌱 **Team Roles**

- **Data Collector & Cleaner**  
  - Collect and prepare datasets, ensuring plant species data is accurate and cleaned for processing.
  - Responsible for partitioning datasets into training, validation, and testing sets.
  
- **Feature Engineer & Model Developer**  
  - Design and build models that accurately classify plant species from images.
  - Work on fine-tuning models (e.g., pre-trained models like EfficientNet) for better accuracy and performance.
  
- **Frontend Developer (Streamlit App)**  
  - Develop the user interface using Streamlit to ensure the app is easy to navigate.
  - Integrate backend functionalities with the frontend, ensuring smooth interaction between the user and the system.
  
- **Backend Developer**  
  - Build the infrastructure for API integration, including the RAG system for plant care information.
  - Ensure data from the Raspberry Pi plant vitals system integrates seamlessly into the app.
---

## **Installation & Setup**

