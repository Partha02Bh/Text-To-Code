import streamlit as st
import cohere
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips
import tempfile

# Initialize Cohere client
API_KEY = "rujUGkqF0GNqEoaU4ifFy2i7oUlUKT4mAgaoJaG4"  # Replace with your Cohere API key
co = cohere.Client(API_KEY)

def generate_text(prompt):
    """
    Generates text using Cohere API based on the input prompt.
    """
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
    )
    return response.generations[0].text

def create_video_from_text(text):
    """
    Creates a simple video from the given text.
    """
    clips = []
    for i, line in enumerate(text.split('.')):
        if line.strip():
            # Create a text clip for each sentence
            text_clip = TextClip(
                line.strip(),
                fontsize=24,
                color='white',
                size=(720, 480),
                bg_color='black',
                method='label'
            ).set_duration(4)  # Each sentence stays for 4 seconds
            clips.append(text_clip)

    # Combine all clips into a single video
    final_video = concatenate_videoclips(clips)
    return final_video

# Streamlit App
st.title("Text-to-Video with Streamlit and Cohere")

# Input prompt
prompt = st.text_area("Enter a prompt for video content:")

if st.button("Generate Video"):
    if prompt.strip():
        with st.spinner("Generating text..."):
            generated_text = generate_text(prompt)
            st.success("Text generated successfully!")

        with st.spinner("Creating video..."):
            video = create_video_from_text(generated_text)

            # Save video to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
                video.write_videofile(tmpfile.name, fps=24, codec="libx264")
                st.video(tmpfile.name)

            st.success("Video created successfully!")
    else:
        st.error("Please enter a prompt!")

