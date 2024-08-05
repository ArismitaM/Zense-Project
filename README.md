# ⚔️ Army Assistant

## 💡 Problem Statement

Using ML to develop a reliable assistant for the Indian army.

## 🎖 Background

On December 29, 2018, at around 1630 hours, a significant incident occurred along the Line of Control (LoC) in the Kashmir region involving the Indian Army's 8 Bihar Regiment. The incident began when an Indian Army patrol detected suspicious movements near their post in the Nowshera sector, an area known for previous Border Action Team (BAT) operations by Pakistani forces. BAT typically comprises Pakistani special forces and terrorists trained to carry out surprise attacks, overrun Indian posts, and behead soldiers. 

Only one soldier from the Indian army (Sepoy Karmadeo) had noticed this suspicious movement and the terrorists were too close to let the other Indian men in the surrounding bunkers know. The terrorists came from a path that was frequented by the Indian army. It is hard to patrol every path every day and the terrorists used this to their advantage and moved along that path soon after the last patrol there.

The terrorists also made sure to block the routes from other Indian posts leading to the 8 Bihar Regiment. While 5 Pakistani men were busy tackling a soul Indian soldier, the Pakistani men received cover fire from various troops stationed uphill.

The Indian soldiers engaged them in an intense exchange of fire. The Indian troops, utilizing their training and steadfast nature, managed to thwart the BAT assault, inflicting significant casualties on the intruding team.

## 🔎 Overview

Some of the problems the Indian army faced were:
- The path the intruding force came from was a surprise.
- The number of people they were dealing with in the opponent force. (By the time they could estimate the number of terrorists, they were harmfully close)

**Possible solutions**
-  The Pakistani forces who provided cover fire to the combat team had settlements built on the hilltop. Satellite imagery can help detect the type of landscape and any changes that happen over time on the landscape to alert forces.
- It is hard to manually patrol and keep vigil on all the routes at all points in time. So, it may be easier to deploy drones which have live camera relays. This way the machine can detect the number of people on a site faster and also make the army aware of the path the forces are taking.

## 📌 Objectives

- This project uses satellite images to detect the land cover in an area. 
- This also uses the BotSort algorithm to detect people and trace the path they take.

## 📊 Technical Aspects
A detailed explanation of the technologies used in this project is as follows:
1. [Land Cover](https://github.com/ArismitaM/Zense-Project/blob/main/LandCover.md)
2. [Path Tracking](https://github.com/ArismitaM/Zense-Project/blob/main/PathTrack.md) 

## 📝 Challenges Faced
- This was my first time dealing with .tif images (satellite images are usually in this format). It took some time to figure out how to do clustering, extracting layers, and draw bounding boxes.
- I could obtain satellite images of Europe and not the Indian subcontinent for the training process.  
- The GPU in my machine does not have enough memory required to train the RetinaNet model, so I had to switch to training with CPU for RetinaNet.
- The BotSort and ByteTrack algorithms were close competitors in theory but gave slightly different outputs when run on the machine.

## 🚀 Future Scope
The incident on 29th December 2018 was the second time a BAT operation was inflicted on the Indian side after many cease-fire violations. As I am writing this, a BAT combat took place just a couple of days ago (in 2024). This shows that this type of attack is a recurring phenomenon and I hope the army can deploy a few aspects of this project in the future.

The Kargil War had taken place when the Pakistani forces claimed territory on the Indian side and made their own settlements when the Indian army had vacated their posts in the harsh winter. It would have been easier for the Indian army if they had known the number of people stationed at the vantage point from the opposing forces, the settlements they had made, and the direction in which they were proceeding to cause casualties.

This shows that this type of tension in the border regions is of serious concern. In such places where manpower is limited, it would be helpful if machines were made to do the monitoring and detection work while humans spent more time training.

## 📈 Further Improvements
- This project will yield better results if the machine can train longer on more powerful computers (instead of on my machine which has limited capability) and have satellite images available of the Indian subcontinent.
- The path tracking part of the project can be extended to gait recognition. It is easy of disguise someone but hard to change the way a person walks. This will help to alert and detect specific people in disguise. 

## Demo video
