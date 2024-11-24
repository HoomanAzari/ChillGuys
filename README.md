# ChillGuys - AI Chat Assistant for Car Dealerships

Welcome to the ChillGuys project! This repository showcases our submission for the CodeJam14 hackathon, where we've developed an AI chat assistant designed to make car dealership inquiries relaxed, fun, and efficient.

## Project Overview

ChillGuys is an AI-powered chat assistant inspired by the "Chill Guy" meme, also known as "My New Character." The assistant embodies a laid-back persona, providing a friendly and approachable experience to help customers find their perfect car.

### Why We Chose This Persona

We chose the "Chill Guy" persona for the AI because of his immense popularity and likability on social media, where countless memes highlight his laid-back, approachable nature. His relaxed demeanor resonates with people, making him the perfect choice to create an engaging and easygoing interaction experience. By adopting his personality, the AI becomes relatable and fun, encouraging customers to feel comfortable while discussing their car needs.

## Features

- **Relaxed and Friendly Persona:** The AI maintains a chill, easygoing vibe to make customers feel at ease during their interaction.
- **Concise and Clear Responses:** Provides fun answers while ensuring the customer receives all the essential information.
- **Tailored Vehicle Recommendations:** Analyzes customer needs and suggests vehicles that best match their preferences.
- **Identity Consistency:** When asked about its identity, the AI replies: *"My whole deal is that I'm a chill guy that lowkey dgaf but I'm here to help you find your ideal car."*

## Technology Stack

### Frontend

The ChillGuys web application is powered by a blend of cutting-edge technologies designed to deliver an exceptional user experience:

- **Frontend:** Built using JavaScript, HTML, and CSS to craft a sleek and aesthetic user interface. 
  - The design theme is cozy, featuring a minimalist yet visually stunning aesthetic, complemented by chill background music that sets a relaxed vibe.
  - The interface is incredibly user-friendly and supports responsive media, ensuring a seamless experience on mobile devices, so you can browse cars effortlessly on the go.

### Backend

- **RESTful API:** The backend implements a RESTful API to facilitate seamless communication with the frontend. RESTful APIs are ideal for scalability, simplicity, and easy integration, making them a great choice for modern web applications.
- **LLM Integration:** 
  - The backend runs locally on a cloud compute engine instance to ensure full control and freedom while avoiding dependency on API keys.
  - Utilizes Ollama to install and manage Llama 3 and Llama 3.2:1b models:
    - **Llama 3** serves as the AI assistant.
    - **Llama 3.2:1b** is used for embedding and managing database entries.
- **LangChain:** The integration of LangChain enables robust functionality for both LLMs, ensuring smooth performance and efficient data handling.
- **Personalized Prompt Engineering:** A tailored prompt has been crafted to perfectly align with the Chill Guy persona, ensuring every interaction reflects the assistant’s relaxed and helpful character.

## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/HoomanAzari/ChillGuys.git
   cd ChillGuys
   ```

2. **Setup Environment:**
   Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   Start the server:
   ```bash
   python app.py
   ```

4. **Interact with the AI:**
   Access the application via the designated interface (e.g., web app, API, or command-line interface) to chat with the ChillGuys assistant.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

We extend our gratitude to the CodeJam14 organizers for providing this platform and to our team for their dedication and creativity.

## Contact

Have questions or feedback? Reach out to Hooman Azari & Imad Issafras at hooazari@gmail.com and imad.issafras@outlook.com, respectively.

---

Get ready to chill with My New Character and discover your next ride in a chill way!
