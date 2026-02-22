from flask import Flask, request, render_template, jsonify, url_for
from flask_cors import CORS
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Class names for plant diseases
class_names = [
    "Apple_Apple_scab", "Apple_Black_rot", "Apple_Cedar_apple_rust", "Apple_healthy",
    "Blueberry_healthy", "Cherry_(including_sour)_Powdery_mildew", "Cherry_(including_sour)_healthy",
    "Corn_(maize)_Cercospora_leaf_spot_Gray_leaf_spot", "Corn_(maize)_Common_rust",
    "Corn_(maize)_Northern_Leaf_Blight", "Corn_(maize)_healthy", "Grape_Black_rot",
    "Grape_Esca_(Black_Measles)", "Grape_Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape_healthy",
    "Orange_Haunglongbing_(Citrus_greening)", "Peach_Bacterial_spot", "Peach_healthy",
    "Pepper,_bell_Bacterial_spot", "Pepper,_bell_healthy", "Potato_Early_blight",
    "Potato_Late_blight", "Potato_healthy", "Raspberry_healthy", "Soybean_healthy",
    "Squash_Powdery_mildew", "Strawberry_Leaf_scorch", "Strawberry_healthy",
    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight", "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot", "Tomato_Spider_mites_Two-spotted_spider_mite", "Tomato_Target_Spot",
    "Tomato_Tomato_Yellow_Leaf_Curl_Virus", "Tomato_Tomato_mosaic_virus", "Tomato_healthy"
]

# Disease treatments dictionary
disease_treatments = {
        "Apple_healthy": {
            "name": "Healthy Apple",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Continue regular monitoring",
                "Maintain good cultural practices",
                "Follow seasonal care guidelines",
                "Practice preventive measures",
                "Ensure proper nutrition"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Compost tea",
                    "usage": "Apply monthly as preventive measure to boost immunity"
                }
            },
            "severity": "None"
        },
        "Apple_Apple_scab": {
            "name": "Apple Scab",
            "description": "Fungal disease causing dark, scaly lesions on leaves and fruit",
            "treatment": [
                "Remove and destroy fallen leaves",
                "Prune to improve air circulation",
                "Water at the base to keep foliage dry",
                "Maintain proper tree spacing",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Captan or Myclobutanil",
                    "usage": "Apply every 7-10 days from green tip stage"
                },
                "organic": {
                    "name": "Neem oil + Copper sulfate mixture",
                    "usage": "Mix 2 tbsp neem oil and 1 tbsp copper sulfate per gallon, apply weekly"
                }
            },
            "severity": "High"
        },
        "Apple_Black_rot": {
            "name": "Apple Black Rot",
            "description": "Fungal disease affecting leaves, fruit, and bark with dark lesions",
            "treatment": [
                "Remove infected fruit and cankers",
                "Prune dead or infected branches",
                "Improve air circulation",
                "Clean up fallen fruit and leaves",
                "Maintain tree vigor"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Thiophanate-methyl",
                    "usage": "Apply at 10-14 day intervals during growing season"
                },
                "organic": {
                    "name": "Bordeaux mixture",
                    "usage": "Apply 4-4-50 mixture during dormant season and early spring"
                }
            },
            "severity": "High"
        },
        "Apple_Cedar_apple_rust": {
            "name": "Cedar Apple Rust",
            "description": "Fungal disease causing bright orange spots on leaves",
            "treatment": [
                "Remove nearby cedar trees if possible",
                "Apply fungicides preventatively",
                "Maintain good air circulation",
                "Clean up fallen leaves",
                "Choose resistant varieties"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Propiconazole",
                    "usage": "Apply from pink bud stage through spring infection period"
                },
                "organic": {
                    "name": "Sulfur + Kelp extract mixture",
                    "usage": "Apply organic sulfur with kelp extract every 7-10 days during growing season"
                }
            },
            "severity": "Moderate"
        },
        "Blueberry_healthy": {
            "name": "Healthy Blueberry",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Maintain proper soil pH (4.5-5.5)",
                "Ensure adequate mulching",
                "Provide proper irrigation",
                "Regular pruning",
                "Monitor for pest activity"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Seaweed extract + Fish emulsion",
                    "usage": "Apply monthly as preventive measure and growth stimulant"
                }
            },
            "severity": "None"
        },
        "Cherry_(including_sour)_Powdery_mildew": {
            "name": "Cherry Powdery Mildew",
            "description": "Fungal disease causing white powdery coating on leaves",
            "treatment": [
                "Improve air circulation",
                "Prune affected areas",
                "Avoid overhead irrigation",
                "Remove infected leaves",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Potassium bicarbonate",
                    "usage": "Apply weekly during growing season when conditions favor disease"
                },
                "organic": {
                    "name": "Milk spray solution + Garlic extract",
                    "usage": "Mix 40% milk with 60% water and garlic extract, apply weekly"
                }
            },
            "severity": "Moderate"
        },
        "Cherry_(including_sour)_healthy": {
            "name": "Healthy Cherry",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular pruning for air circulation",
                "Maintain proper fertilization",
                "Monitor for early signs of issues",
                "Proper irrigation practices",
                "Seasonal maintenance"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Compost tea + Seaweed extract",
                    "usage": "Apply monthly for prevention and plant vigor"
                }
            },
            "severity": "None"
        },
        "Corn_(maize)_Cercospora_leaf_spot": {
            "name": "Gray Leaf Spot",
            "description": "Fungal disease causing rectangular gray lesions on corn leaves",
            "treatment": [
                "Rotate crops with non-host plants",
                "Remove crop debris",
                "Improve air circulation",
                "Plant resistant hybrids",
                "Time planting to avoid high disease periods"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Azoxystrobin",
                    "usage": "Apply at first sign of disease and repeat at 14-day intervals"
                },
                "organic": {
                    "name": "Bacillus subtilis + Neem oil",
                    "usage": "Apply mixture every 7-10 days during growing season"
                }
            },
            "severity": "High"
        },
        "Corn_(maize)_Common_rust": {
            "name": "Common Rust",
            "description": "Fungal disease causing small, red to brown pustules",
            "treatment": [
                "Plant resistant hybrids",
                "Monitor fields regularly",
                "Time planting appropriately",
                "Maintain proper fertility",
                "Apply fungicides if necessary"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Pyraclostrobin",
                    "usage": "Apply when rust first appears and repeat at 7-14 day intervals"
                },
                "organic": {
                    "name": "Copper octanoate + Essential oils",
                    "usage": "Apply organic copper solution with tea tree oil every 7-10 days"
                }
            },
            "severity": "Moderate"
        },
        "Corn_(maize)_Northern_Leaf_Blight": {
            "name": "Northern Leaf Blight",
            "description": "Fungal disease causing long, cigar-shaped lesions",
            "treatment": [
                "Plant resistant varieties",
                "Rotate crops",
                "Remove crop debris",
                "Improve air circulation",
                "Time planting to avoid disease"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Trifloxystrobin",
                    "usage": "Apply when disease first appears and repeat at 7-14 day intervals"
                },
                "organic": {
                    "name": "Streptomyces lydicus + Compost tea",
                    "usage": "Apply beneficial bacteria mixture every 7-10 days"
                }
            },
            "severity": "High"
        },
        "Corn_(maize)_healthy": {
            "name": "Healthy Corn",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Maintain proper fertility",
                "Ensure adequate irrigation",
                "Monitor for pest activity",
                "Practice crop rotation",
                "Control weeds"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Seaweed extract + Humic acid",
                    "usage": "Apply monthly for soil and plant health"
                }
            },
            "severity": "None"
        },
        "Grape_Black_rot": {
            "name": "Grape Black Rot",
            "description": "Fungal disease causing black lesions on leaves and fruit",
            "treatment": [
                "Remove mummified berries",
                "Prune for air circulation",
                "Clean up fallen debris",
                "Manage canopy density",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Mancozeb",
                    "usage": "Apply from bud break until veraison at 7-14 day intervals"
                },
                "organic": {
                    "name": "Copper hydroxide + Neem oil",
                    "usage": "Mix 2 tbsp each per gallon, apply every 7-14 days"
                }
            },
            "severity": "High"
        },
        "Grape_Esca_(Black_Measles)": {
            "name": "Grape Esca",
            "description": "Complex fungal disease affecting woody tissue",
            "treatment": [
                "Remove infected vines",
                "Proper pruning techniques",
                "Avoid stress conditions",
                "Maintain vine vigor",
                "Use clean pruning tools"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Trichoderma formulations",
                    "usage": "Apply to pruning wounds to prevent infection"
                },
                "organic": {
                    "name": "Beneficial fungi mixture + Seaweed extract",
                    "usage": "Apply to wounds and soil, repeat monthly"
                }
            },
            "severity": "Severe"
        },
        "Grape_Leaf_blight": {
            "name": "Grape Leaf Blight",
            "description": "Fungal disease causing brown spots with dark borders",
            "treatment": [
                "Improve air circulation",
                "Remove infected leaves",
                "Manage irrigation",
                "Proper canopy management",
                "Apply fungicides when needed"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Copper hydroxide",
                    "usage": "Apply at 7-14 day intervals during growing season"
                },
                "organic": {
                    "name": "Garlic extract + Neem oil",
                    "usage": "Apply mixture weekly during growing season"
                }
            },
            "severity": "Moderate"
        },
        "Grape_healthy": {
            "name": "Healthy Grape",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular pruning",
                "Proper fertilization",
                "Maintain good air flow",
                "Monitor for early issues",
                "Practice proper irrigation"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Kelp extract + Compost tea",
                    "usage": "Apply monthly for prevention and plant health"
                }
            },
            "severity": "None"
        },
        "Orange_Haunglongbing": {
            "name": "Citrus Greening",
            "description": "Bacterial disease spread by Asian citrus psyllid",
            "treatment": [
                "Remove infected trees",
                "Control psyllid populations",
                "Use disease-free nursery stock",
                "Regular monitoring",
                "Maintain tree health"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Imidacloprid",
                    "usage": "Apply systemically to control psyllid populations"
                },
                "organic": {
                    "name": "Pyrethrin + Neem oil",
                    "usage": "Apply mixture every 7-10 days for psyllid control"
                }
            },
            "severity": "Severe"
        },
        "Peach_Bacterial_spot": {
            "name": "Peach Bacterial Spot",
            "description": "Bacterial disease causing spots on fruit and leaves",
            "treatment": [
                "Prune during dry weather",
                "Improve air circulation",
                "Avoid overhead irrigation",
                "Remove infected tissue",
                "Apply copper sprays"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Copper compounds",
                    "usage": "Apply during leaf fall and dormant season"
                },
                "organic": {
                    "name": "Bacterial antagonists + Copper soap",
                    "usage": "Apply mixture every 7-14 days during growing season"
                }
            },
            "severity": "High"
        },
        "Peach_healthy": {
            "name": "Healthy Peach",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular pruning",
                "Proper fertilization",
                "Maintain good air flow",
                "Monitor for issues",
                "Practice proper irrigation"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Fish emulsion + Seaweed extract",
                    "usage": "Apply monthly for prevention and nutrition"
                }
            },
            "severity": "None"
        },
        "Pepper_bell_Bacterial_spot": {
            "name": "Pepper Bacterial Spot",
            "description": "Bacterial disease causing spots on leaves and fruit",
            "treatment": [
                "Rotate crops",
                "Avoid overhead irrigation",
                "Remove infected plants",
                "Improve air circulation",
                "Use disease-free seeds"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Copper-based bactericide",
                    "usage": "Apply weekly during wet periods"
                },
                "organic": {
                    "name": "Bacillus subtilis + Copper soap",
                    "usage": "Apply mixture every 5-7 days during wet weather"
                }
            },
            "severity": "High"
        },
        "Pepper_bell_healthy": {
            "name": "Healthy Bell Pepper",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular monitoring",
                "Proper spacing",
                "Adequate fertilization",
                "Weed control",
                "Proper irrigation"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Compost tea + Kelp extract",
                    "usage": "Apply monthly for prevention and growth"
                }
            },
            "severity": "None"
        },
        "Potato_Early_blight": {
            "name": "Potato Early Blight",
            "description": "Fungal disease causing dark brown spots with concentric rings",
            "treatment": [
                "Rotate crops",
                "Remove infected leaves",
                "Improve air circulation",
                "Avoid overhead irrigation",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Chlorothalonil",
                    "usage": "Apply every 7-10 days during growing season"
                },
                "organic": {
                    "name": "Copper sulfate + Neem oil",
                    "usage": "Apply mixture weekly during growing season"
                }
            },
            "severity": "Moderate"
        },
        "Potato_Late_blight": {
            "name": "Potato Late Blight",
            "description": "Fungal disease causing water-soaked lesions that turn brown",
            "treatment": [
                "Remove infected plants",
                "Improve drainage",
                "Plant resistant varieties",
                "Monitor weather conditions",
                "Apply preventative fungicides"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Mefenoxam",
                    "usage": "Apply every 5-7 days during wet conditions"
                },
                "organic": {
                    "name": "Copper hydroxide + Bacillus subtilis",
                    "usage": "Apply mixture every 5-7 days during wet weather"
                }
            },
            "severity": "Severe"
        },
        "Potato_healthy": {
            "name": "Healthy Potato",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular hilling",
                "Proper spacing",
                "Adequate fertilization",
                "Weed control",
                "Monitor soil moisture"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Fish emulsion + Seaweed extract",
                    "usage": "Apply monthly for plant nutrition"
                }
            },
            "severity": "None"
        },
        "Raspberry_healthy": {
            "name": "Healthy Raspberry",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular pruning",
                "Proper trellising",
                "Adequate mulching",
                "Control weeds",
                "Maintain proper spacing"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Compost tea + Kelp extract",
                    "usage": "Apply monthly for prevention and vigor"
                }
            },
            "severity": "None"
        },
        "Soybean_healthy": {
            "name": "Healthy Soybean",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Proper row spacing",
                "Adequate fertilization",
                "Weed management",
                "Regular monitoring",
                "Maintain soil health"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Rhizobia inoculant + Seaweed extract",
                    "usage": "Apply at planting and monthly thereafter"
                }
            },
            "severity": "None"
        },
        "Squash_Powdery_mildew": {
            "name": "Squash Powdery Mildew",
            "description": "Fungal disease causing white powdery coating on leaves",
            "treatment": [
                "Improve air circulation",
                "Avoid overhead watering",
                "Remove infected leaves",
                "Plant resistant varieties",
                "Apply fungicides early"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Potassium bicarbonate",
                    "usage": "Apply weekly when conditions favor disease"
                },
                "organic": {
                    "name": "Milk spray + Neem oil",
                    "usage": "Mix 40% milk with water and neem oil, apply weekly"
                }
            },
            "severity": "Moderate"
        },
        "Strawberry_Leaf_scorch": {
            "name": "Strawberry Leaf Scorch",
            "description": "Fungal disease causing purple to red spots with brown centers",
            "treatment": [
                "Remove infected leaves",
                "Improve air circulation",
                "Avoid overhead irrigation",
                "Proper plant spacing",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Captan",
                    "usage": "Apply every 7-10 days during growing season"
                },
                "organic": {
                    "name": "Copper soap + Bacillus subtilis",
                    "usage": "Apply mixture weekly during growing season"
                }
            },
            "severity": "Moderate"
        },
        "Strawberry_healthy": {
            "name": "Healthy Strawberry",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular mulching",
                "Proper spacing",
                "Adequate fertilization",
                "Weed control",
                "Monitor irrigation"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Compost tea + Fish emulsion",
                    "usage": "Apply monthly for prevention and nutrition"
                }
            },
            "severity": "None"
        },
        "Tomato_Bacterial_spot": {
            "name": "Tomato Bacterial Spot",
            "description": "Bacterial disease causing dark, raised spots on leaves and fruit",
            "treatment": [
                "Remove infected plants",
                "Rotate crops",
                "Avoid overhead irrigation",
                "Improve air circulation",
                "Use disease-free seeds"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Copper-based bactericide",
                    "usage": "Apply every 7-10 days during wet conditions"
                },
                "organic": {
                    "name": "Copper soap + Bacillus subtilis",
                    "usage": "Apply mixture weekly during growing season"
                }
            },
            "severity": "High"
        },
        "Tomato_Early_blight": {
            "name": "Tomato Early Blight",
            "description": "Fungal disease causing dark brown spots with concentric rings",
            "treatment": [
                "Remove lower infected leaves",
                "Improve air circulation",
                "Mulch around plants",
                "Proper plant spacing",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Chlorothalonil",
                    "usage": "Apply every 7-14 days during growing season"
                },
                "organic": {
                    "name": "Copper sulfate + Neem oil",
                    "usage": "Mix and apply weekly during growing season"
                }
            },
            "severity": "Moderate"
        },
        "Tomato_Late_blight": {
            "name": "Tomato Late Blight",
            "description": "Fungal disease causing large dark brown patches with white edges",
            "treatment": [
                "Remove infected plants immediately",
                "Improve drainage",
                "Space plants properly",
                "Monitor weather conditions",
                "Apply preventative fungicides"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Mancozeb",
                    "usage": "Apply every 5-7 days during wet conditions"
                },
                "organic": {
                    "name": "Copper hydroxide + Beneficial bacteria",
                    "usage": "Apply mixture every 5-7 days during wet weather"
                }
            },
            "severity": "Severe"
        },
        "Tomato_Leaf_Mold": {
            "name": "Tomato Leaf Mold",
            "description": "Fungal disease causing yellow spots and olive-green mold on leaves",
            "treatment": [
                "Reduce humidity",
                "Improve ventilation",
                "Remove infected leaves",
                "Space plants properly",
                "Apply fungicides when needed"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Chlorothalonil",
                    "usage": "Apply every 7-14 days when conditions favor disease"
                },
                "organic": {
                    "name": "Potassium bicarbonate + Neem oil",
                    "usage": "Apply mixture weekly during humid conditions"
                }
            },
            "severity": "Moderate"
        },
        "Tomato_Septoria_leaf_spot": {
            "name": "Tomato Septoria Leaf Spot",
            "description": "Fungal disease causing small circular spots with dark borders",
            "treatment": [
                "Remove infected leaves",
                "Mulch around plants",
                "Improve air circulation",
                "Avoid overhead watering",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Copper fungicide",
                    "usage": "Apply every 7-10 days during growing season"
                },
                "organic": {
                    "name": "Copper soap + Compost tea",
                    "usage": "Apply mixture weekly during growing season"
                }
            },
            "severity": "High"
        },
        "Tomato_Spider_mites_Two-spotted_spider_mite": {
            "name": "Two-spotted Spider Mites",
            "description": "Tiny arachnids causing stippling on leaves and fine webbing",
            "treatment": [
                "Increase humidity",
                "Spray plants with water",
                "Remove heavily infested leaves",
                "Introduce predatory mites",
                "Apply miticides if severe"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Bifenthrin",
                    "usage": "Apply every 7 days until controlled"
                },
                "organic": {
                    "name": "Insecticidal soap + Neem oil",
                    "usage": "Apply mixture every 3-5 days until controlled"
                }
            },
            "severity": "High"
        },
        "Tomato_Target_Spot": {
            "name": "Tomato Target Spot",
            "description": "Fungal disease causing brown circular spots with concentric rings",
            "treatment": [
                "Remove infected leaves",
                "Improve air circulation",
                "Avoid leaf wetness",
                "Proper plant spacing",
                "Apply fungicides preventatively"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Azoxystrobin",
                    "usage": "Apply every 7-14 days during growing season"
                },
                "organic": {
                    "name": "Copper sulfate + Bacterial antagonists",
                    "usage": "Apply mixture weekly during growing season"
                }
            },
            "severity": "High"
        },
        "Tomato_Yellow_Leaf_Curl_Virus": {
            "name": "Tomato Yellow Leaf Curl Virus",
            "description": "Viral disease causing yellowing, curling leaves and stunted growth",
            "treatment": [
                "Remove infected plants",
                "Control whitefly vectors",
                "Use resistant varieties",
                "Install physical barriers",
                "Maintain weed control"
            ],
            "pesticide": {
                "chemical": {
                    "name": "Imidacloprid",
                    "usage": "Apply as soil drench for whitefly control"
                },
                "organic": {
                    "name": "Pyrethrin + Neem oil",
                    "usage": "Apply mixture every 5-7 days for whitefly control"
                }
            },
            "severity": "Severe"
        },
        "Tomato_mosaic_virus": {
            "name": "Tomato Mosaic Virus",
            "description": "Viral disease causing mottled and distorted leaves",
            "treatment": [
                "Remove infected plants",
                "Control aphid vectors",
                "Use virus-free seeds",
                "Sanitize tools",
                "Plant resistant varieties"
            ],
            "pesticide": {
                "chemical": {
                    "name": "No effective chemical control",
                    "usage": "Focus on prevention and vector control"
                },
                "organic": {
                    "name": "Insecticidal soap + Pyrethrin",
                    "usage": "Apply for aphid control every 5-7 days"
                }
            },
            "severity": "Severe"
        },
        "Tomato_healthy": {
            "name": "Healthy Tomato",
            "description": "Plant appears healthy with no visible disease symptoms",
            "treatment": [
                "Regular pruning",
                "Proper staking",
                "Adequate fertilization",
                "Monitor irrigation",
                "Maintain good airflow"
            ],
            "pesticide": {
                "chemical": {
                    "name": "None required",
                    "usage": "Monitor and apply only if problems develop"
                },
                "organic": {
                    "name": "Seaweed extract + Compost tea",
                    "usage": "Apply monthly for prevention and plant health"
                }
            },
            "severity": "None"
        }
    }


# Healthy plant labels
healthy_plants = [
    "Apple_healthy", "Blueberry_healthy", "Cherry_(including_sour)_healthy",
    "Corn_(maize)_healthy", "Grape_healthy", "Peach_healthy", "Pepper,_bell_healthy",
    "Potato_healthy", "Raspberry_healthy", "Soybean_healthy", "Strawberry_healthy", "Tomato_healthy"
]

# Directory to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# FAQ for chatbot
faq = [
    # Common Symptoms and Identification
    {
        "question": "What are the common symptoms of plant diseases?",
        "answer": "Common symptoms include yellowing leaves, spots on leaves, wilting, stunted growth, and moldy growth on stems or leaves."
    },
    {
        "question": "How can I identify if my plant is diseased?",
        "answer": "Look for abnormal changes like discoloration, spots, wilting, or stunted growth. Use our detection system to confirm the disease."
    },
    {
        "question": "Can I identify the disease by just looking at the plant?",
        "answer": "Visual inspection can help, but a detection system ensures accurate identification."
    },
    {
        "question": "Is there a tool to identify plant diseases?",
        "answer": "Yes, you can upload an image to our system for a quick diagnosis."
    },
    {
        "question": "Does the system detect all plant diseases?",
        "answer": "Our model detects 38 plant diseases, including common ones for potatoes, tomatoes, corn, peaches, and apples."
    },

    # Prevention and Care
    {
        "question": "How can I prevent fungal infections in plants?",
        "answer": "Ensure proper drainage, avoid overwatering, and use fungicides like copper-based sprays in recommended quantities."
    },
    {
        "question": "How can I prevent plant diseases?",
        "answer": "Maintain good soil health, use disease-resistant varieties, and avoid overwatering."
    },
    {
        "question": "What are the best practices for plant health?",
        "answer": "Rotate crops, prune regularly, and ensure adequate sunlight and ventilation."
    },
    {
        "question": "Does soil quality affect diseases?",
        "answer": "Yes, poor soil drainage and nutrient deficiencies can lead to diseases."
    },
    {
        "question": "Are organic methods effective for disease prevention?",
        "answer": "Yes, practices like composting and using natural repellents help prevent diseases."
    },
    {
        "question": "Should I remove diseased plants from the field?",
        "answer": "Yes, promptly remove and dispose of infected plants to prevent the disease from spreading."
    },

    # Treatment and Chemicals
    {
        "question": "What should I do if my plant is diseased?",
        "answer": "Use the recommended treatment and follow chemical application instructions provided by the model."
    },
    {
        "question": "What pesticide should I use for aphids?",
        "answer": "You can use neem oil or insecticidal soap. Apply as per the manufacturer's instructions."
    },
    {
        "question": "What chemicals should I use for treatment?",
        "answer": "The system provides specific chemicals based on the detected disease."
    },
    {
        "question": "How should I apply the chemicals?",
        "answer": "Mix the recommended chemical in the suggested proportion with water and spray uniformly."
    },
    {
        "question": "Are the recommended chemicals safe for the environment?",
        "answer": "The suggested chemicals are approved for agricultural use and are environmentally safe if applied correctly."
    },
    {
        "question": "How often should I apply the chemicals?",
        "answer": "Follow the frequency specified by the system, usually once every 7-10 days."
    },

    # Crop-Specific Questions
    {
        "question": "What are common diseases in potato plants?",
        "answer": "Diseases include late blight, early blight, and bacterial wilt."
    },
    {
        "question": "How do I treat blight in tomatoes?",
        "answer": "Use fungicides containing copper or chlorothalonil as recommended."
    },
    {
        "question": "What are common apple tree diseases?",
        "answer": "Apple scab, powdery mildew, and fire blight are common diseases."
    },
    {
        "question": "How can I prevent rust in corn plants?",
        "answer": "Use resistant varieties and apply fungicides during the early stages of infection."
    },
    {
        "question": "Are peach trees prone to fungal infections?",
        "answer": "Yes, peach leaf curl and brown rot are common fungal diseases."
    },

    # Environmental Factors
    {
        "question": "Does temperature affect plant diseases?",
        "answer": "Yes, many diseases thrive in warm, humid conditions."
    },
    {
        "question": "What are ideal conditions for healthy plant growth?",
        "answer": "Adequate sunlight, well-drained soil, and balanced watering are key."
    },
    {
        "question": "Does overwatering cause diseases?",
        "answer": "Yes, overwatering leads to root rot and fungal infections."
    },
    {
        "question": "Can wind spread plant diseases?",
        "answer": "Yes, wind can carry spores and spread infections."
    },
    {
        "question": "Does the season affect plant diseases?",
        "answer": "Certain diseases are more prevalent in specific seasons due to favorable environmental conditions."
    },

    # General Usage
    {
        "question": "How do I upload a picture of my plant?",
        "answer": "You upload an image in the website's Plant disease detection section for a detailed analysis."
    },
    {
        "question": "How does your plant disease detection system work?",
        "answer": "Upload an image of the diseased plant, and our model will analyze and provide results."
    },
    {
        "question": "Is the system easy to use for beginners?",
        "answer": "Yes, the interface is user-friendly and provides clear instructions."
    },
    {
        "question": "What do I need to use the detection system?",
        "answer": "You need a clear image of the diseased plant and an internet connection to access the system."
    },
    {
        "question": "Can the system suggest organic solutions?",
        "answer": "Currently, it focuses on chemical treatments, but organic recommendations can be added."
    },
    {
        "question": "Can I get detailed precautions for each disease?",
        "answer": "No"
    }
]

@app.route('/')
def home():
    """Render the home page with the upload form and chatbot."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        image = request.files['image']
        location = request.form.get('location')
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        # Placeholder result since the AI model is removed
        disease_info = {
            "name": "AI Analysis (Maintenance)",
            "description": "The AI detection engine is currently offline to save resources. Use the chatbot below for help!",
            "treatment": ["Ensure proper watering", "Check soil pH", "Monitor for pests"],
            "severity": "N/A"
        }
        return render_template(
            'result.html',
            result=disease_info,
            location=location,
            image_url=url_for('static', filename=f'uploads/{image.filename}')
        )
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot interactions."""
    user_input = request.json.get("message", "").lower()

    if not user_input:
        return jsonify({"reply": "Please ask a question!"})

    for item in faq:
        if item["question"].lower() in user_input:
            return jsonify({"reply": item["answer"]})

    return jsonify({"reply": "I'm sorry, I don't have information on that. Can you provide more details?"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
