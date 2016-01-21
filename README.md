## How to automatically assigns tags to these events. 

In order to classify each and every scraped event to the respective tag it belongs, lets throw some light on what we are trying to achive here.
Lets say I am avid puzzle solver and jigsaw puzzles are something what i love.
I have collected thousands of puzzle sets since my childhood, and over the time things are cluster F**ng mess and jigsaw pizzes are scatterd all across my home.
Now I intend to keep seprate boxes for all the 1000 puzzle sets each containing jigsaw beices belonging to that puzzle.
So, I pick up a piece of puzzle and I have to take decision right then which box is most likely to contain this piece.
I will start with analyzing the puzzle with features such as color, size of peice , etcs which help me identify and build a mental model which puzzle is this peice most likely to fit in.
Lets say puzzle piece I picked is blue in colors and there is pirate flag visible on that piece , so I can catagorized this puzzle piece as a part of Sea Voyage Puzzle.
My likely hood of classifying each piece will increase with the ammount of experience I had with the puzzles.

Since the goal in information retrieval is to find the best document given a query, one could decide to model the probability of a document given particular query.
Hence, in the puzzle example mentioned above , this would mean we are trying to do direct mapping from appearnce puzzle peiece to a box is needed.
 We need to calculate of likelyhood of the box given a piece or in this case 'extracted_event' to tag.
 
 example 
    P(Sports| cheered) ~ higer probability
    P(Politics| cheered) ~ not very high likelyhood
    
Hence for each and every scraped event , we have to do NER on that event to 
find even referencing phrases
 
Event Referring Phrases:
• Useful to display in connection with events
- E.g. “iPhone” + “launched” + “October 6”
• Helpful in categorizing Events into Types

Examples:
Apple to Announce iPhone 5 on October 4th! YES!
iPhone 5 announcement coming Oct 4th
WOOOHOO NEW IPHONE TODAY! CAN’T WAIT! 

### Categorizing Event Types
• Would like to categorize events into
types, for example:
- Sports
- Politics
- Music

### Classifying Events Challenges :
• Many Different Types
• Not sure what is the right set of types
• Set of types might change
– Might start talking about different things
– Might want to focus on different groups of users

 
### Annotating Named Entities
  tweeted_on : [20th November 2016] date
  [Kanye West]p ruined [MTV Europe Music Awards]event [2016]occurence date
  In annotating NER , we have to do this either manualy or for specific domain which enables the System to have a training set to refer to, when scraping new events.
  But there is lot of manual work in this approach.

### Unsupervised Event Type Induction
• Latent Variable Models
- Generative Probabilistic Models ( the one I talked about at the begining)

• Advantages:
- Discovers types which match the data
- No need to annotate individual events
- Don’t need to commit to a specific set of types
- Modular, can integrate into various applications

However Each Event Phrase is modeled as a mixture of types, here we do probilistic determination of each named entity, to identify mapping of that entity to specific tag 
  P(SPORTS|cheered)= 0.6
  P(POLITICS|cheered)= 0.4

Each Event Type phrase is associated with modeled as a distribution mixture of other Entities, Types and Dates

I have added a python script, which I have written earlier to do NER on Tweets <https://github.com/aregee/scrappy/blob/master/ner.py>

The python code helps to classify tweets in the following categories:
   ['LOCATION', 'PERSON', 'FACILITY', 'GSP', 'ORGANIZATION', 'GPE']
Below is data produced by the script, on the recent tweets near my geo location
```
{
  "data": {
    "hashtags": [
      [
        "#Property",
        3
      ],
      [
        "#india",
        3
      ],
      [
        "#Noida",
        3
      ],
      [
        "#Flat",
        3
      ],
      [
        "#NewDelhi",
        2
      ],
      [
        "#Residential",
        2
      ],
      [
        "#Gurgaon",
        2
      ],
      [
        "#ForRent",
        2
      ],
      [
        "#WowMSG2MSG2",
        2
      ],
      [
        "#Resi",
        1
      ],
      [
        "#airlifton22ndjan",
        1
      ],
      [
        "#SaritaVihar,",
        1
      ],
      [
        "#CareerArc",
        1
      ],
      [
        "#photomariefrayssinet",
        1
      ],
      [
        "#Apartment",
        1
      ],
      [
        "#city",
        1
      ],
      [
        "#Rajasthan",
        1
      ],
      [
        "#morning",
        1
      ],
      [
        "#kitavegetariankakak",
        1
      ],
      [
        "#AZADI",
        1
      ],
      [
        "#bikaner",
        1
      ],
      [
        "#Jaipur",
        1
      ],
      [
        "#goodearth",
        1
      ],
      [
        "#JSA",
        1
      ],
      [
        "#Sector162",
        1
      ],
      [
        "#Jobs",
        1
      ],
      [
        "#Lonelyplanet",
        1
      ],
      [
        "#Land",
        1
      ],
      [
        "#Commercial",
        1
      ],
      [
        "#amberfort",
        1
      ],
      [
        "#Sector45",
        1
      ],
      [
        "#ResidentialPlot",
        1
      ],
      [
        "#Neu-Delhi",
        1
      ],
      [
        "#be",
        1
      ],
      [
        "#job?",
        1
      ],
      [
        "#incredibleindia",
        1
      ],
      [
        "#Indepedence#IndepedenceOfMind/Soul",
        1
      ],
      [
        "#adayintheworld",
        1
      ],
      [
        "#goodmorning",
        1
      ],
      [
        "#Respect",
        1
      ],
      [
        "#ForSale",
        1
      ],
      [
        "#Quran",
        1
      ],
      [
        "#Ghaziabad",
        1
      ],
      [
        "#dessert",
        1
      ],
      [
        "#2BHK",
        1
      ],
      [
        "#VaibhavKhand",
        1
      ],
      [
        "#snapdeal",
        1
      ],
      [
        "#orange\u2026",
        1
      ],
      [
        "#Air",
        1
      ],
      [
        "#Shop",
        1
      ],
      [
        "#quiz",
        1
      ],
      [
        "#FreeChargeInEverySale",
        1
      ],
      [
        "#4BHK",
        1
      ],
      [
        "#Job:",
        1
      ],
      [
        "#ForSale.",
        1
      ],
      [
        "#rajasthan",
        1
      ],
      [
        "#lunchtime",
        1
      ],
      [
        "#pink",
        1
      ],
      [
        "#Hiring",
        1
      ],
      [
        "#millionshadesofindia\u2026",
        1
      ]
    ],
    "links": [
      [
        "https://t.co/MQRmfcar0W",
        1
      ],
      [
        "https://t.co/W1UZZI8EXr",
        1
      ],
      [
        "https://t.co/HUzjAsfMo7",
        1
      ],
      [
        "https://t.co/aDjRdVFdj6",
        1
      ],
      [
        "https://t.co/JN4xZwbPj7",
        1
      ],
      [
        "https://t.co/sj4W08NwVU",
        1
      ],
      [
        "https://t.co/EDe2zMqdhV",
        1
      ],
      [
        "https://t.co/KhXQ93x63L",
        1
      ],
      [
        "https://t.co/IaqNfcOdAH",
        1
      ],
      [
        "https://t.co/rTXxP6x9NR",
        1
      ],
      [
        "https://t.co/ipKGMlkY0u",
        1
      ],
      [
        "https://t.co/6UeA17GkeY",
        1
      ],
      [
        "https://t.co/aRLHA9jHVt",
        1
      ],
      [
        "https://t.co/cSvbATv9d3",
        1
      ],
      [
        "https://t.co/2oIxzUlysa",
        1
      ],
      [
        "https://t.co/KaCUrhvdVp",
        1
      ],
      [
        "https://t.co/YRh80WARgo",
        1
      ],
      [
        "https://t.co/VjAwVi15N5",
        1
      ]
    ],
    "mentions": [
      [
        "@pankajTHEbhatia",
        3
      ],
      [
        "@Flw_ur_dreamz",
        2
      ],
      [
        "@hr_shapers",
        1
      ],
      [
        "@StarGoldIndia",
        1
      ],
      [
        "@1Patelzuber",
        1
      ],
      [
        "@cool_bulls",
        1
      ],
      [
        "@Shakir248",
        1
      ],
      [
        "@poonamraniratia",
        1
      ],
      [
        "@PanwarDimple",
        1
      ],
      [
        "@AanchalTripathi",
        1
      ],
      [
        "@IRCTC_Ltd",
        1
      ],
      [
        "@insanfamily1",
        1
      ],
      [
        "@RaviAwasthi",
        1
      ]
    ],
    "ner": {
      "GPE": {
        "Delhi": {
          "count": 1,
          "tweet_ids": [
            690084388172926976
          ]
        },
        "Good": {
          "count": 1,
          "tweet_ids": [
            690085581234249729
          ]
        },
        "INDIA": {
          "count": 1,
          "tweet_ids": [
            690088905757036544
          ]
        },
        "Janam": {
          "count": 1,
          "tweet_ids": [
            690085744262680576
          ]
        },
        "Modi": {
          "count": 1,
          "tweet_ids": [
            690088998023368706
          ]
        },
        "Oglio": {
          "count": 1,
          "tweet_ids": [
            690086707597832192
          ]
        },
        "Palace": {
          "count": 1,
          "tweet_ids": [
            690086219707977728
          ]
        },
        "Wo": {
          "count": 1,
          "tweet_ids": [
            690083923683049472
          ]
        }
      },
      "ORGANIZATION": {
        "Chocolate": {
          "count": 1,
          "tweet_ids": [
            690085201024847873
          ]
        },
        "Comfort My Soul": {
          "count": 1,
          "tweet_ids": [
            690086727701155841
          ]
        },
        "DDA Flats": {
          "count": 1,
          "tweet_ids": [
            690085517292146688
          ]
        },
        "DayOneIsAllowed2sayDifferently2Act": {
          "count": 1,
          "tweet_ids": [
            690087769331388416
          ]
        },
        "Employees": {
          "count": 1,
          "tweet_ids": [
            690086949059706881
          ]
        },
        "Fiserv": {
          "count": 1,
          "tweet_ids": [
            690083002785857536
          ]
        },
        "GPTW": {
          "count": 1,
          "tweet_ids": [
            690086949059706881
          ]
        },
        "Health": {
          "count": 1,
          "tweet_ids": [
            690086949059706881
          ]
        },
        "IndepedenceOnEarthWillBeThe": {
          "count": 1,
          "tweet_ids": [
            690087769331388416
          ]
        },
        "Parsvnath Majestic Arcade": {
          "count": 1,
          "tweet_ids": [
            690085272562831362
          ]
        },
        "SQFT Center Park": {
          "count": 1,
          "tweet_ids": [
            690087456339841024
          ]
        },
        "Shalimar Garden": {
          "count": 1,
          "tweet_ids": [
            690086707597832192
          ]
        },
        "WAHEGURU Give Me Hope": {
          "count": 1,
          "tweet_ids": [
            690086727701155841
          ]
        },
        "WOMEN": {
          "count": 1,
          "tweet_ids": [
            690082785944604672
          ]
        }
      },
      "PERSON": {
        "Ahhhh": {
          "count": 1,
          "tweet_ids": [
            690084388172926976
          ]
        },
        "Bikaner": {
          "count": 1,
          "tweet_ids": [
            690088905757036544
          ]
        },
        "Free": {
          "count": 1,
          "tweet_ids": [
            690086949059706881
          ]
        },
        "Network Engineer": {
          "count": 1,
          "tweet_ids": [
            690085601341784068
          ]
        },
        "None": {
          "count": 1,
          "tweet_ids": [
            690086727701155841
          ]
        },
        "Prateek": {
          "count": 1,
          "tweet_ids": [
            690087456339841024
          ]
        },
        "Prem": {
          "count": 1,
          "tweet_ids": [
            690088953186275329
          ]
        },
        "Ready": {
          "count": 1,
          "tweet_ids": [
            690087456339841024
          ]
        },
        "Shahpurjat": {
          "count": 1,
          "tweet_ids": [
            690084388172926976
          ]
        },
        "Technical": {
          "count": 1,
          "tweet_ids": [
            690083002785857536
          ]
        },
        "Truffle Cake": {
          "count": 1,
          "tweet_ids": [
            690085201024847873
          ]
        },
        "Twitter": {
          "count": 2,
          "tweet_ids": [
            690082451155189761,
            690082234393559041
          ]
        }
      }
    }
  }
}

```
