# Player Image Recognition (with RAG)

A lightweight implementation of RAG (Retrieval-Augmented Generation) pipline that centers on facial recognition of football player. 


## Project Description

The project takes users through the full lifecyle — from scraping player images from Getty Images, generating face embeddings with DeepFace and storing them in Pinecone, to querying the system with a new image to identify the player. 

The backend of the project is built with **FastAPI**, where each endpoint is connected to a dedicated module for scraping, embedding, and querying. On the frontend, the interface is rendered by **React** to allow users to upload images and receive real-time identification results through API calls to the backend.  

## Project Demo

[![Project Walkthrough](https://img.youtube.com/vi/b1Xy86wlR20/0.jpg)](https://www.youtube.com/watch?v=b1Xy86wlR20)
