# VisionAI

Application de description vidéo en temps réel avec synthèse vocale multilingue (Anglais, Français, Wolof).

## Table des matières

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Architecture technique](#architecture-technique)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Limites connues](#limites-connues)

---

## Présentation

VisionAI capture le flux de la webcam en temps réel et génère automatiquement une description textuelle de chaque scène toutes les 5 secondes. La description est traduite en français et en wolof, puis convertie en audio dans la langue choisie par l'utilisateur.

Ce projet vise à améliorer l'accessibilité et à démontrer l'usage de l'intelligence artificielle pour la compréhension visuelle dans des langues locales africaines.

---

## Fonctionnalités

- Capture et analyse du flux webcam en temps réel
- Génération automatique de descriptions en anglais via le modèle BLIP (Salesforce)
- Traduction instantanée vers le français et le wolof
- Synthèse vocale dans la langue sélectionnée (gTTS)
- Affichage de la description en surimpression sur la vidéo
- Gestion et suppression des fichiers audio générés
- Accélération GPU automatique si disponible (CUDA)

---

## Architecture technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Interface web | Streamlit | 1.33.0 |
| Vision par ordinateur | OpenCV | 4.11.0 |
| Modèle de description | BLIP (Hugging Face Transformers) | 4.48.3 |
| Deep learning | PyTorch | 2.2.2 |
| Traitement d'images | Pillow | 10.2.0 |
| Traduction | MyMemory API (gratuite) | - |
| Synthèse vocale | gTTS (Google Text-to-Speech) | 2.5.4 |
| Calcul numérique | NumPy | 1.26.4 |

---

## Prérequis

- Python 3.9 ou supérieur
- Une webcam fonctionnelle
- Connexion internet (pour la traduction MyMemory et la synthèse vocale gTTS)
- (Optionnel) GPU NVIDIA avec CUDA pour de meilleures performances

Dépendances système (Linux) :

```bash
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

---

## Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/Aminata11052000/VisionAI.git
cd VisionAI
```

2. Créer et activer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

3. Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

4. Lancer l'application :

```bash
streamlit run app2.py
```

L'application sera accessible à l'adresse `http://localhost:8501`.

---

## Utilisation

1. Ouvrir l'application dans le navigateur.
2. Cocher "Demarrer la video" pour activer la capture webcam.
3. Sélectionner la langue souhaitée : Anglais, Français ou Wolof.
4. Une description est générée toutes les 5 secondes, affichée en surimpression sur la vidéo et lue en audio.
5. Les fichiers audio générés apparaissent en haut de la page et peuvent être supprimés individuellement.

---

## Structure du projet

```
VisionAI/
├── app2.py              # Application principale (Streamlit)
├── requirements.txt     # Dépendances Python
├── packages.txt         # Dépendances système (déploiement Streamlit Cloud)
└── README.md
```

---

## Limites connues

- Le wolof n'est pas pris en charge nativement par gTTS : la synthèse vocale utilise le moteur français comme approximation.
- L'API MyMemory est gratuite et soumise à un quota quotidien limité.
- L'application n'est pas conçue pour un déploiement multi-utilisateurs en raison de l'accès direct à la webcam.
