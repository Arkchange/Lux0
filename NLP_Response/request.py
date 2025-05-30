import requests
import time

start = time.time()

url = "https://ml-inference-service-558315166056.europe-west1.run.app/predict"
payload = {
  "features": ["Merci pour votre candidature. Nous souhaiterions vous rencontrer pour un entretien afin d'échanger davantage sur votre profil. Merci de nous indiquer vos disponibilités cette semaine.",
  "Après examen de votre candidature, nous avons le regret de vous informer que votre profil n’a pas été retenu pour ce poste.Nous vous remercions pour l'intérêt porté à notre entreprise.",
  "Suite à nos échanges et votre entretien, nous sommes heureux de vous proposer le poste de Data Analyst Junior. Vous trouverez ci-joint les documents nécessaires à la suite du processus.Au plaisir de vous compter parmi nous",
"Nous vous remercions pour votre candidature. Vous êtes convié(e) à un entretien technique le [date/heure], en visioconférence. Merci de confirmer votre présence.",
"Nous avons bien reçu votre candidature. Après analyse, nous avons décidé de ne pas donner suite à votre profil pour ce poste.Nous vous souhaitons une bonne continuation.",
"Nous vous remercions pour le temps consacré à nos échanges. Nous avons le plaisir de vous informer que vous êtes retenu(e) pour la prochaine étape du processus de recrutement.",
"Malgré l’intérêt que présente votre profil, nous avons décidé de poursuivre avec d’autres candidatures. Nous vous remercions pour votre démarche et restons disponibles pour un retour.",
"Nous avons le plaisir de vous annoncer que vous avez été sélectionné(e) pour rejoindre notre équipe en tant que Data Scientist Junior. Merci de bien vouloir confirmer votre acceptation avant le [date].",
"Votre candidature a retenu notre attention. Nous souhaitons organiser un entretien RH afin d’échanger sur vos motivations et votre parcours. Merci de nous proposer vos disponibilités.",
]
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
end = time.time()

print("Request duration:", end - start, "seconds")
print("Status code:", response.status_code)
print("Response JSON:", response.json())
