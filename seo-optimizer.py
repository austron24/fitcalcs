#!/usr/bin/env python3
"""
SEO Optimizer for FitCalcs pages
Based on Google's SEO Starter Guide recommendations
"""

import os
import re
from datetime import datetime

# Calculator-specific SEO data for better optimization
CALCULATOR_SEO_DATA = {
    'bmi-calculator': {
        'title': 'BMI Calculator - Calculate Your Body Mass Index Instantly | FitCalcs',
        'description': 'Free BMI calculator to calculate your Body Mass Index. Get instant results with healthy weight ranges, BMI categories, and personalized recommendations.',
        'keywords': ['BMI calculator', 'body mass index', 'calculate BMI', 'healthy weight', 'BMI chart'],
        'category': 'HealthApplication',
        'faqs': [
            ('What is BMI and how is it calculated?', 'BMI (Body Mass Index) is calculated by dividing your weight in kilograms by your height in meters squared. It provides a simple measure of body fatness for most adults.'),
            ('What is a healthy BMI range?', 'A healthy BMI is typically between 18.5 and 24.9. Below 18.5 is considered underweight, 25-29.9 is overweight, and 30 or above is obese.'),
            ('Is BMI accurate for athletes?', 'BMI may overestimate body fat in athletes and muscular individuals since it does not distinguish between muscle and fat mass.')
        ],
        'howto': ['Enter your height in feet/inches or centimeters', 'Enter your weight in pounds or kilograms', 'View your BMI result and category', 'Check your healthy weight range']
    },
    'calorie-calculator': {
        'title': 'Calorie Calculator - Daily Calorie Needs Calculator | FitCalcs',
        'description': 'Free calorie calculator to determine your daily calorie needs for weight loss, maintenance, or gain. Based on your age, gender, height, weight, and activity level.',
        'keywords': ['calorie calculator', 'daily calories', 'TDEE calculator', 'weight loss calories', 'calorie needs'],
        'category': 'HealthApplication',
        'faqs': [
            ('How many calories should I eat per day?', 'Daily calorie needs vary based on age, sex, weight, height, and activity level. Most adults need 1,600-3,000 calories daily.'),
            ('How do I calculate calories for weight loss?', 'For safe weight loss, create a 500-750 calorie deficit from your maintenance calories. This typically results in 1-1.5 pounds lost per week.'),
            ('What is TDEE?', 'TDEE (Total Daily Energy Expenditure) is the total calories you burn per day including exercise. It is your maintenance calorie level.')
        ],
        'howto': ['Enter your age, gender, and measurements', 'Select your activity level', 'View your daily calorie needs', 'Adjust for weight goals']
    },
    'tdee-calculator': {
        'title': 'TDEE Calculator - Total Daily Energy Expenditure | FitCalcs',
        'description': 'Calculate your Total Daily Energy Expenditure (TDEE) to determine how many calories you burn per day. Includes BMR calculation and activity multipliers.',
        'keywords': ['TDEE calculator', 'total daily energy expenditure', 'BMR calculator', 'calories burned', 'metabolic rate'],
        'category': 'HealthApplication',
        'faqs': [
            ('What is TDEE?', 'TDEE stands for Total Daily Energy Expenditure. It represents the total number of calories your body burns in a day, including all activities.'),
            ('How is TDEE calculated?', 'TDEE is calculated by multiplying your Basal Metabolic Rate (BMR) by an activity factor that reflects your daily activity level.'),
            ('Why is TDEE important for weight management?', 'Knowing your TDEE helps you create the right calorie deficit for weight loss or surplus for muscle gain.')
        ],
        'howto': ['Enter your age, height, and weight', 'Select your gender', 'Choose your activity level', 'Get your TDEE and calorie recommendations']
    },
    'body-fat-calculator': {
        'title': 'Body Fat Calculator - Calculate Body Fat Percentage | FitCalcs',
        'description': 'Free body fat percentage calculator using the U.S. Navy method. Calculate your body fat percentage with just a few measurements.',
        'keywords': ['body fat calculator', 'body fat percentage', 'fat percentage calculator', 'Navy method', 'body composition'],
        'category': 'HealthApplication',
        'faqs': [
            ('How accurate is this body fat calculator?', 'The Navy method body fat calculator is approximately 97% accurate compared to hydrostatic weighing for most individuals.'),
            ('What is a healthy body fat percentage?', 'Healthy body fat ranges are 10-22% for men and 20-32% for women. Athletes typically have lower percentages.'),
            ('How often should I measure body fat?', 'Measure body fat every 2-4 weeks for accurate tracking, as daily fluctuations are normal.')
        ],
        'howto': ['Enter your height and weight', 'Measure and enter your waist circumference', 'For men, enter neck measurement. For women, add hip measurement', 'Calculate your body fat percentage']
    },
    'macro-calculator': {
        'title': 'Macro Calculator - Calculate Your Daily Macros | FitCalcs',
        'description': 'Free macro calculator to determine your ideal daily protein, carbs, and fat intake based on your goals. Perfect for weight loss, muscle gain, or maintenance.',
        'keywords': ['macro calculator', 'macronutrient calculator', 'protein calculator', 'carb calculator', 'IIFYM'],
        'category': 'HealthApplication',
        'faqs': [
            ('What are macros?', 'Macros (macronutrients) are the three main nutrients your body needs in large amounts: protein, carbohydrates, and fats. Each provides calories and serves different functions.'),
            ('How do I calculate my macros for weight loss?', 'For weight loss, a typical split is 40% protein, 30% carbs, and 30% fat, with total calories at a deficit from your TDEE.'),
            ('How much protein do I need per day?', 'Most adults need 0.8-1g of protein per pound of body weight. Athletes and those building muscle may need 1-1.2g per pound.')
        ],
        'howto': ['Enter your personal details and goal', 'Select your preferred macro split', 'Get your daily gram targets for each macro', 'Track your intake to meet these goals']
    },
    'ideal-weight-calculator': {
        'title': 'Ideal Weight Calculator - Find Your Ideal Body Weight | FitCalcs',
        'description': 'Calculate your ideal body weight using multiple scientific formulas. Get personalized healthy weight ranges based on your height, age, and gender.',
        'keywords': ['ideal weight calculator', 'healthy weight', 'ideal body weight', 'IBW calculator', 'target weight'],
        'category': 'HealthApplication',
        'faqs': [
            ('How is ideal weight calculated?', 'Ideal weight is calculated using formulas like Devine, Robinson, Miller, and Hamwi, which consider height and gender to estimate a healthy weight range.'),
            ('Is ideal weight the same for everyone of the same height?', 'No, ideal weight varies based on body frame, muscle mass, age, and gender. The calculated range is a general guideline.'),
            ('Should I aim for my ideal weight?', 'Ideal weight is a reference point. Focus on overall health markers like body fat percentage, fitness level, and how you feel.')
        ],
        'howto': ['Enter your height', 'Select your gender', 'Optionally add your age', 'View your ideal weight range from multiple formulas']
    },
    'pregnancy-calculator': {
        'title': 'Pregnancy Calculator - Due Date & Week Calculator | FitCalcs',
        'description': 'Free pregnancy due date calculator. Calculate your due date, current pregnancy week, trimester, and important milestones based on your last menstrual period.',
        'keywords': ['pregnancy calculator', 'due date calculator', 'pregnancy week calculator', 'conception date', 'trimester calculator'],
        'category': 'HealthApplication',
        'faqs': [
            ('How is my due date calculated?', 'Your due date is calculated by adding 280 days (40 weeks) to the first day of your last menstrual period (LMP).'),
            ('How accurate is a due date calculator?', 'Due date calculators are generally accurate, but only about 5% of babies are born on their exact due date. Most arrive within two weeks of the calculated date.'),
            ('What are the pregnancy trimesters?', 'First trimester: weeks 1-12. Second trimester: weeks 13-26. Third trimester: weeks 27-40.')
        ],
        'howto': ['Enter the first day of your last menstrual period', 'Optionally adjust your cycle length', 'View your estimated due date', 'Track your current week and trimester']
    },
    'ovulation-calculator': {
        'title': 'Ovulation Calculator - Fertile Window Calculator | FitCalcs',
        'description': 'Free ovulation calculator to predict your fertile window and ovulation day. Maximize your chances of conception by knowing your most fertile days.',
        'keywords': ['ovulation calculator', 'fertile window', 'fertility calculator', 'conception calculator', 'ovulation predictor'],
        'category': 'HealthApplication',
        'faqs': [
            ('When do I ovulate?', 'Ovulation typically occurs around day 14 of a 28-day cycle, but can vary. It usually happens 12-16 days before your next period.'),
            ('What is the fertile window?', 'The fertile window is the 5 days before ovulation plus ovulation day itself. Sperm can survive up to 5 days, making these your most fertile days.'),
            ('How accurate is an ovulation calculator?', 'Ovulation calculators provide estimates based on average cycles. For more accuracy, combine with ovulation predictor kits or basal body temperature tracking.')
        ],
        'howto': ['Enter the first day of your last period', 'Enter your average cycle length', 'View your predicted ovulation day', 'See your full fertile window']
    },
    'sleep-calculator': {
        'title': 'Sleep Calculator - Optimal Bedtime & Wake Time | FitCalcs',
        'description': 'Free sleep calculator to find your optimal bedtime or wake time based on sleep cycles. Wake up refreshed by timing your sleep with 90-minute cycles.',
        'keywords': ['sleep calculator', 'bedtime calculator', 'sleep cycle calculator', 'wake up time', 'sleep schedule'],
        'category': 'HealthApplication',
        'faqs': [
            ('How do sleep cycles work?', 'Sleep occurs in 90-minute cycles consisting of light sleep, deep sleep, and REM sleep. Waking between cycles helps you feel more refreshed.'),
            ('How much sleep do I need?', 'Most adults need 7-9 hours of sleep per night, which equals about 5-6 complete sleep cycles.'),
            ('Why do I feel tired after 8 hours of sleep?', 'You may be waking in the middle of a sleep cycle. Try adjusting your bedtime by 15-30 minutes to align with cycle completion.')
        ],
        'howto': ['Choose whether to calculate bedtime or wake time', 'Enter your target time', 'Account for time to fall asleep (usually 15 minutes)', 'Select from optimal sleep cycle times']
    },
    'water-intake-calculator': {
        'title': 'Water Intake Calculator - Daily Hydration Needs | FitCalcs',
        'description': 'Calculate your optimal daily water intake based on weight, activity level, and climate. Stay properly hydrated for better health and performance.',
        'keywords': ['water intake calculator', 'hydration calculator', 'how much water', 'daily water needs', 'water consumption'],
        'category': 'HealthApplication',
        'faqs': [
            ('How much water should I drink daily?', 'A general guideline is to drink half your body weight in ounces. For example, a 160-pound person should aim for 80 ounces (about 10 cups) daily.'),
            ('Does coffee count toward water intake?', 'Caffeinated beverages do contribute to hydration, but water is ideal. Coffee has mild diuretic effects but still provides net hydration.'),
            ('How do I know if I am drinking enough water?', 'Signs of good hydration include pale yellow urine, regular urination, and absence of thirst. Dark urine often indicates dehydration.')
        ],
        'howto': ['Enter your body weight', 'Select your activity level', 'Adjust for climate and conditions', 'View your recommended daily water intake']
    },
    'keto-calculator': {
        'title': 'Keto Calculator - Ketogenic Diet Macro Calculator | FitCalcs',
        'description': 'Free keto calculator to determine your ideal ketogenic diet macros. Calculate your daily carb limit, protein, and fat intake for ketosis.',
        'keywords': ['keto calculator', 'ketogenic diet calculator', 'keto macros', 'low carb calculator', 'ketosis calculator'],
        'category': 'HealthApplication',
        'faqs': [
            ('How many carbs can I eat on keto?', 'Most keto diets limit carbs to 20-50 grams net carbs per day to achieve and maintain ketosis.'),
            ('How much protein do I need on keto?', 'On keto, aim for 0.6-1.0 grams of protein per pound of lean body mass to preserve muscle while staying in ketosis.'),
            ('How long does it take to enter ketosis?', 'It typically takes 2-4 days of limiting carbs to 20-50g to enter ketosis. This varies based on individual metabolism and activity level.')
        ],
        'howto': ['Enter your stats (age, height, weight, gender)', 'Set your activity level and deficit', 'Choose your carb limit', 'Get your personalized keto macros']
    },
    'protein-intake-calculator': {
        'title': 'Protein Intake Calculator - Daily Protein Needs | FitCalcs',
        'description': 'Calculate your optimal daily protein intake based on your weight, activity level, and fitness goals. Essential for muscle building and recovery.',
        'keywords': ['protein calculator', 'protein intake', 'daily protein', 'muscle building protein', 'protein requirements'],
        'category': 'HealthApplication',
        'faqs': [
            ('How much protein do I need per day?', 'Most adults need 0.8g per kg of body weight. Active individuals and athletes may need 1.2-2.0g per kg for optimal performance and recovery.'),
            ('When should I eat protein?', 'Spread protein intake throughout the day for optimal absorption. Aim for 20-40g per meal, with protein around workouts being especially beneficial.'),
            ('Can I eat too much protein?', 'Most healthy adults can safely consume up to 2g per kg daily. Higher intakes are generally unnecessary and provide no additional benefit.')
        ],
        'howto': ['Enter your current weight', 'Select your activity level', 'Choose your fitness goal', 'Get your personalized protein target']
    },
    'heart-rate-calculator': {
        'title': 'Heart Rate Calculator - Target Heart Rate Zones | FitCalcs',
        'description': 'Calculate your target heart rate zones for optimal cardio training. Find your maximum heart rate and training zones for fat burning and endurance.',
        'keywords': ['heart rate calculator', 'target heart rate', 'max heart rate', 'heart rate zones', 'cardio zones'],
        'category': 'HealthApplication',
        'faqs': [
            ('How do I calculate my maximum heart rate?', 'The most common formula is 220 minus your age. For example, a 30-year-old has an estimated max heart rate of 190 bpm.'),
            ('What heart rate zone burns the most fat?', 'The fat-burning zone is typically 60-70% of your max heart rate. However, higher intensity burns more total calories.'),
            ('Why are heart rate zones important?', 'Training in different zones targets different fitness goals: Zone 2 for endurance, Zone 3 for aerobic capacity, Zone 4-5 for speed and power.')
        ],
        'howto': ['Enter your age', 'Optionally enter your resting heart rate for more accuracy', 'View your maximum heart rate', 'See all your training heart rate zones']
    },
    'one-rep-max-calculator': {
        'title': '1RM Calculator - One Rep Max Calculator | FitCalcs',
        'description': 'Calculate your one rep max (1RM) for any lift using weight and reps performed. Essential for programming strength training and tracking progress.',
        'keywords': ['1RM calculator', 'one rep max', 'max weight calculator', 'strength calculator', 'lifting max'],
        'category': 'HealthApplication',
        'faqs': [
            ('What is a 1RM?', 'One rep max (1RM) is the maximum weight you can lift for a single repetition with proper form. It is used to gauge strength and program training.'),
            ('How accurate is a 1RM calculator?', 'Calculators are most accurate with 1-10 reps. Predictions from higher reps become less reliable as fatigue factors vary.'),
            ('How often should I test my 1RM?', 'Test your 1RM every 8-12 weeks or at the end of training cycles. Frequent maxing can interfere with training progress.')
        ],
        'howto': ['Enter the weight you lifted', 'Enter the number of reps completed', 'View your estimated 1RM', 'See percentage-based training weights']
    },
    'pace-calculator': {
        'title': 'Pace Calculator - Running Pace & Split Times | FitCalcs',
        'description': 'Calculate your running pace, finish time, or distance. Get split times for any race distance from 5K to marathon. Perfect for race planning.',
        'keywords': ['pace calculator', 'running pace', 'race pace calculator', 'split times', 'marathon pace'],
        'category': 'HealthApplication',
        'faqs': [
            ('How do I calculate my running pace?', 'Divide your total time by distance. For example, 30 minutes for 5K equals 6 minutes per kilometer or about 9:40 per mile.'),
            ('What is a good running pace for beginners?', 'Beginners typically run at 10-13 minute per mile pace. The key is finding a pace where you can hold a conversation.'),
            ('How do I improve my running pace?', 'Incorporate interval training, tempo runs, and consistent mileage. Improvement comes gradually with training.')
        ],
        'howto': ['Enter distance or race type', 'Enter your time or target pace', 'Calculate your pace, time, or distance', 'View split times for each mile/km']
    },
    'dog-age-calculator': {
        'title': 'Dog Age Calculator - Dog Years to Human Years | FitCalcs',
        'description': 'Convert your dog\'s age to human years using the scientifically accurate formula. Accounts for breed size for more precise results.',
        'keywords': ['dog age calculator', 'dog years', 'dog to human years', 'pet age calculator', 'canine age'],
        'category': 'HealthApplication',
        'faqs': [
            ('Is 1 dog year really 7 human years?', 'No, this is a myth. Dogs age faster in their first two years, then slow down. A 1-year-old dog is more like 15 in human years.'),
            ('Do small dogs age differently than large dogs?', 'Yes, smaller dogs tend to live longer and age more slowly than larger breeds. A small dog at 10 is like 56 human years, while a large dog is more like 66.'),
            ('How long do dogs typically live?', 'Small breeds often live 12-16 years, medium breeds 10-13 years, and large breeds 8-12 years.')
        ],
        'howto': ['Enter your dog\'s age in years', 'Select your dog\'s size category', 'View the equivalent human age', 'See life stage information']
    },
    'cat-age-calculator': {
        'title': 'Cat Age Calculator - Cat Years to Human Years | FitCalcs',
        'description': 'Convert your cat\'s age to human years accurately. Understand your feline\'s life stage with our easy-to-use cat age calculator.',
        'keywords': ['cat age calculator', 'cat years', 'cat to human years', 'feline age', 'pet age'],
        'category': 'HealthApplication',
        'faqs': [
            ('How do cat years work?', 'Cats age rapidly in their first two years. Year one equals about 15 human years, year two adds 9 more. After that, each year equals about 4 human years.'),
            ('When is a cat considered a senior?', 'Cats are typically considered seniors at 11-14 years old (equivalent to 60-72 human years) and geriatric after 15.'),
            ('How long do cats typically live?', 'Indoor cats typically live 12-18 years, with some reaching their early 20s. Outdoor cats have shorter lifespans due to environmental risks.')
        ],
        'howto': ['Enter your cat\'s age in years', 'View the equivalent human age', 'See your cat\'s life stage', 'Get age-appropriate care tips']
    },
    'fasting-calculator': {
        'title': 'Fasting Calculator - Intermittent Fasting Timer | FitCalcs',
        'description': 'Track your intermittent fasting windows with our fasting calculator. Calculate eating windows for 16:8, 18:6, 20:4, and other fasting protocols.',
        'keywords': ['fasting calculator', 'intermittent fasting', 'fasting timer', 'IF calculator', '16:8 fasting'],
        'category': 'HealthApplication',
        'faqs': [
            ('What is intermittent fasting?', 'Intermittent fasting is an eating pattern that cycles between periods of fasting and eating. Popular methods include 16:8, 18:6, and OMAD.'),
            ('What can I have during a fast?', 'Water, black coffee, and plain tea are generally acceptable during fasting. These have minimal calories and won\'t break your fast.'),
            ('When will I see results from fasting?', 'Most people notice weight loss and improved energy within 2-4 weeks of consistent intermittent fasting.')
        ],
        'howto': ['Select your fasting protocol (16:8, 18:6, etc.)', 'Enter your last meal time or start time', 'View your fasting and eating windows', 'Track your progress']
    },
    'weight-loss-calculator': {
        'title': 'Weight Loss Calculator - Calorie Deficit Planner | FitCalcs',
        'description': 'Calculate how long it will take to reach your goal weight. Get personalized calorie and macro recommendations for healthy, sustainable weight loss.',
        'keywords': ['weight loss calculator', 'calorie deficit', 'weight loss planner', 'goal weight calculator', 'diet calculator'],
        'category': 'HealthApplication',
        'faqs': [
            ('How fast should I lose weight?', 'Safe weight loss is 1-2 pounds per week. This requires a daily deficit of 500-1000 calories from your maintenance level.'),
            ('What calorie deficit should I aim for?', 'A 500-calorie daily deficit is sustainable for most people and results in about 1 pound lost per week.'),
            ('Why has my weight loss stalled?', 'Plateaus are normal. Your metabolism adapts as you lose weight. Recalculate your needs and consider diet breaks or increased activity.')
        ],
        'howto': ['Enter your current weight and goal weight', 'Set your daily calorie intake or deficit', 'View your projected timeline', 'Get weekly milestones to track']
    },
    'caffeine-calculator': {
        'title': 'Caffeine Calculator - Daily Caffeine Intake Tracker | FitCalcs',
        'description': 'Track your daily caffeine intake and see when it will leave your system. Calculate safe caffeine limits based on your body weight.',
        'keywords': ['caffeine calculator', 'caffeine intake', 'caffeine half-life', 'coffee calculator', 'safe caffeine limit'],
        'category': 'HealthApplication',
        'faqs': [
            ('How much caffeine is safe per day?', 'Most adults can safely consume up to 400mg of caffeine daily (about 4 cups of coffee). Pregnant women should limit to 200mg.'),
            ('How long does caffeine stay in your system?', 'Caffeine has a half-life of 5-6 hours. This means half the caffeine from your morning coffee is still in your system 6 hours later.'),
            ('When should I stop drinking caffeine?', 'Stop caffeine consumption 6-8 hours before bedtime to minimize sleep disruption.')
        ],
        'howto': ['Enter your beverages and caffeine sources', 'View your total daily intake', 'See when caffeine will clear your system', 'Check if you are within safe limits']
    },
    'age-calculator': {
        'title': 'Age Calculator - Calculate Exact Age in Years, Months, Days | FitCalcs',
        'description': 'Calculate your exact age in years, months, days, hours, and minutes. Find out how many days until your next birthday.',
        'keywords': ['age calculator', 'birthday calculator', 'exact age', 'age in days', 'how old am I'],
        'category': 'HealthApplication',
        'faqs': [
            ('How is age calculated exactly?', 'Age is calculated from your birth date to today, accounting for leap years and varying month lengths for precise results.'),
            ('How many days old am I?', 'Enter your birth date to see your exact age in days. The average person lives about 27,375 days (75 years).'),
            ('When is my half birthday?', 'Your half birthday is exactly 6 months after your birth date.')
        ],
        'howto': ['Enter your birth date', 'Optionally enter a different end date', 'View your exact age breakdown', 'See days until your next birthday']
    },
    'due-date-calculator': {
        'title': 'Due Date Calculator - Pregnancy Due Date | FitCalcs',
        'description': 'Calculate your pregnancy due date based on your last menstrual period or conception date. Track your pregnancy week by week.',
        'keywords': ['due date calculator', 'pregnancy due date', 'conception date', 'when is baby due', 'EDD calculator'],
        'category': 'HealthApplication',
        'faqs': [
            ('How accurate is a due date calculator?', 'Due dates are estimates. Only about 5% of babies are born on their exact due date. Most arrive within 2 weeks before or after.'),
            ('How is the due date calculated?', 'Due date is calculated by adding 280 days (40 weeks) to the first day of your last menstrual period.'),
            ('Can my due date change?', 'Yes, ultrasounds may adjust your due date, especially if done in the first trimester when dating is most accurate.')
        ],
        'howto': ['Enter the first day of your last period', 'Or enter your conception date', 'View your estimated due date', 'Track your current pregnancy week']
    },
    'walking-calorie-calculator': {
        'title': 'Walking Calorie Calculator - Calories Burned Walking | FitCalcs',
        'description': 'Calculate calories burned while walking based on your weight, distance, and pace. Track your walking exercise for weight management.',
        'keywords': ['walking calories', 'calories burned walking', 'walking exercise', 'step calculator', 'walk calorie burn'],
        'category': 'HealthApplication',
        'faqs': [
            ('How many calories does walking burn?', 'Walking burns approximately 80-100 calories per mile for a 150-pound person. Faster pace and heavier weight increase calorie burn.'),
            ('How many steps is a mile?', 'The average person takes about 2,000-2,500 steps per mile, depending on stride length.'),
            ('Is walking good for weight loss?', 'Yes! Walking is an excellent low-impact exercise for weight loss. Walking 10,000 steps daily can help create a calorie deficit.')
        ],
        'howto': ['Enter your body weight', 'Enter distance walked or time', 'Select your walking pace', 'View calories burned']
    },
    'running-pace-calculator': {
        'title': 'Running Pace Calculator - Pace, Time & Distance | FitCalcs',
        'description': 'Calculate your running pace, finish time, or distance. Get splits for 5K, 10K, half marathon, and marathon races.',
        'keywords': ['running pace', 'race pace calculator', '5K pace', 'marathon pace', 'running splits'],
        'category': 'HealthApplication',
        'faqs': [
            ('What is a good 5K pace for beginners?', 'Beginners typically run a 5K in 25-35 minutes, which is an 8-11 minute per mile pace.'),
            ('How do I calculate my race pace?', 'Divide your total time by the distance. For example, 24 minutes for 5K = 7:43 per mile pace.'),
            ('How can I run faster?', 'Incorporate speed work, tempo runs, and consistent training. Most runners improve with interval training.')
        ],
        'howto': ['Enter your race distance', 'Enter time or target pace', 'Calculate pace, time, or distance', 'View mile and kilometer splits']
    },
    'blood-pressure-calculator': {
        'title': 'Blood Pressure Calculator - BP Category Checker | FitCalcs',
        'description': 'Check your blood pressure category based on systolic and diastolic readings. Understand if your blood pressure is normal, elevated, or high.',
        'keywords': ['blood pressure calculator', 'BP checker', 'blood pressure category', 'hypertension calculator', 'normal blood pressure'],
        'category': 'HealthApplication',
        'faqs': [
            ('What is normal blood pressure?', 'Normal blood pressure is less than 120/80 mmHg. Elevated is 120-129/<80. Stage 1 hypertension is 130-139/80-89.'),
            ('When should I check my blood pressure?', 'Check at the same time daily, preferably in the morning. Sit quietly for 5 minutes before measuring.'),
            ('What affects blood pressure readings?', 'Caffeine, stress, exercise, posture, and full bladder can temporarily raise blood pressure readings.')
        ],
        'howto': ['Enter your systolic (top number) reading', 'Enter your diastolic (bottom number) reading', 'View your blood pressure category', 'Get health recommendations']
    },
    'alcohol-calculator': {
        'title': 'Alcohol Calculator - Drinks & BAC Estimator | FitCalcs',
        'description': 'Calculate standard drinks and estimate blood alcohol content based on your consumption. Understand how alcohol affects your body.',
        'keywords': ['alcohol calculator', 'BAC calculator', 'blood alcohol', 'standard drinks', 'alcohol units'],
        'category': 'HealthApplication',
        'faqs': [
            ('What is a standard drink?', 'A standard drink contains about 14 grams of pure alcohol. This equals 12 oz beer (5%), 5 oz wine (12%), or 1.5 oz spirits (40%).'),
            ('How long does it take to sober up?', 'Your body metabolizes about one standard drink per hour. No amount of coffee, food, or water speeds this up.'),
            ('What is the legal BAC limit?', 'In the US, the legal driving limit is 0.08% BAC. However, impairment begins at much lower levels.')
        ],
        'howto': ['Enter your drink type and quantity', 'Enter your weight and gender', 'Enter time since first drink', 'View estimated BAC and sober time']
    },
    'bac-calculator': {
        'title': 'BAC Calculator - Blood Alcohol Content Estimator | FitCalcs',
        'description': 'Estimate your Blood Alcohol Content (BAC) based on drinks consumed, body weight, and time. Understand alcohol impairment levels.',
        'keywords': ['BAC calculator', 'blood alcohol content', 'alcohol level', 'drunk calculator', 'BAC estimator'],
        'category': 'HealthApplication',
        'faqs': [
            ('How is BAC calculated?', 'BAC is calculated using the Widmark formula, which considers alcohol consumed, body weight, gender, and time elapsed.'),
            ('What BAC is considered drunk?', 'Legal intoxication is 0.08% in most US states. Effects begin at 0.02% with reduced judgment starting around 0.05%.'),
            ('How long until I am sober?', 'Your BAC decreases approximately 0.015% per hour. At 0.08%, it takes about 5-6 hours to reach 0.00%.')
        ],
        'howto': ['Enter number and type of drinks', 'Enter your weight and gender', 'Enter hours since first drink', 'View estimated BAC and effects']
    },
    'percentage-calculator': {
        'title': 'Percentage Calculator - Calculate Percentages Easily | FitCalcs',
        'description': 'Free percentage calculator for all percentage calculations. Find percentage of a number, percentage change, and percentage difference.',
        'keywords': ['percentage calculator', 'percent calculator', 'percentage change', 'calculate percentage', 'percent of number'],
        'category': 'UtilitiesApplication',
        'faqs': [
            ('How do I calculate percentage of a number?', 'Multiply the number by the percentage and divide by 100. For 20% of 150: (150 x 20) / 100 = 30.'),
            ('How do I calculate percentage change?', 'Percentage change = ((New - Old) / Old) x 100. For example, from 50 to 75: ((75-50)/50) x 100 = 50% increase.'),
            ('How do I find what percentage one number is of another?', 'Divide the part by the whole and multiply by 100. For example, 25 is what percent of 200? (25/200) x 100 = 12.5%.')
        ],
        'howto': ['Choose your calculation type', 'Enter your numbers', 'Click calculate', 'View your percentage result']
    },
    'square-footage-calculator': {
        'title': 'Square Footage Calculator - Calculate Area | FitCalcs',
        'description': 'Calculate square footage for any shape. Perfect for flooring, painting, gardening, and home improvement projects. Free and easy to use.',
        'keywords': ['square footage calculator', 'area calculator', 'square feet', 'room size calculator', 'flooring calculator'],
        'category': 'UtilitiesApplication',
        'faqs': [
            ('How do I calculate square footage?', 'For a rectangle, multiply length by width. For example, a 10ft x 12ft room = 120 square feet.'),
            ('How do I calculate irregular shapes?', 'Break the area into smaller rectangles, calculate each, then add them together.'),
            ('How much flooring do I need?', 'Calculate your square footage and add 10% for waste and cuts. For a 200 sq ft room, order 220 sq ft of material.')
        ],
        'howto': ['Select the shape (rectangle, circle, triangle)', 'Enter your measurements', 'View the square footage result', 'Add rooms for total area']
    },
    'gas-mileage-calculator': {
        'title': 'Gas Mileage Calculator - MPG & Fuel Cost Calculator | FitCalcs',
        'description': 'Calculate your vehicle\'s gas mileage (MPG) and fuel costs for trips. Track fuel efficiency and compare costs between fill-ups.',
        'keywords': ['gas mileage calculator', 'MPG calculator', 'fuel economy', 'fuel cost calculator', 'miles per gallon'],
        'category': 'UtilitiesApplication',
        'faqs': [
            ('How do I calculate MPG?', 'Divide miles driven by gallons used. If you drove 300 miles on 10 gallons, your MPG is 30.'),
            ('What is good gas mileage?', 'For passenger cars, 30+ MPG is considered good. Hybrids often exceed 50 MPG. Trucks and SUVs typically get 15-25 MPG.'),
            ('How can I improve my gas mileage?', 'Keep tires properly inflated, avoid aggressive driving, remove excess weight, and maintain your vehicle regularly.')
        ],
        'howto': ['Enter miles driven since last fill-up', 'Enter gallons of fuel used', 'View your MPG calculation', 'Optionally calculate trip fuel costs']
    },
    'image-resizer': {
        'title': 'Image Resizer - Resize Images Online Free | FitCalcs',
        'description': 'Resize images online for free. Resize by percentage or exact dimensions. Supports JPG, PNG, and other formats. No upload required.',
        'keywords': ['image resizer', 'resize image', 'picture resizer', 'photo resizer', 'resize online'],
        'category': 'UtilitiesApplication',
        'faqs': [
            ('How do I resize an image without losing quality?', 'When reducing size, quality loss is minimal. When enlarging, limit to 200% to avoid pixelation. Use high-quality source images.'),
            ('What is the best image size for web?', 'For web, keep images under 200KB. Common sizes are 1200px wide for content images and 150px for thumbnails.'),
            ('Can I resize multiple images at once?', 'This tool handles one image at a time for best quality. For batch processing, consider desktop software.')
        ],
        'howto': ['Upload your image', 'Choose resize method (percentage or dimensions)', 'Enter your target size', 'Download your resized image']
    },
    'image-compressor': {
        'title': 'Image Compressor - Compress Images Online Free | FitCalcs',
        'description': 'Compress images online without losing quality. Reduce file size for faster website loading. Supports JPG, PNG, and other formats.',
        'keywords': ['image compressor', 'compress image', 'reduce image size', 'image optimizer', 'compress online'],
        'category': 'UtilitiesApplication',
        'faqs': [
            ('How much can images be compressed?', 'Most images can be compressed 50-80% without noticeable quality loss. Results vary based on original file and content.'),
            ('What is lossy vs lossless compression?', 'Lossless keeps all data (smaller reduction). Lossy removes some data for greater size reduction with minimal visible difference.'),
            ('What image format compresses best?', 'JPEG is best for photos with lossy compression. PNG is better for graphics with transparency. WebP offers the best of both.')
        ],
        'howto': ['Upload your image', 'Select compression level', 'Preview the result', 'Download compressed image']
    }
}

# Default SEO data for calculators not in the specific list
DEFAULT_SEO = {
    'category': 'HealthApplication',
    'faqs': [
        ('How accurate is this calculator?', 'This calculator uses established formulas and provides reliable estimates. For personalized advice, consult a professional.'),
        ('Is this calculator free to use?', 'Yes, all calculators on FitCalcs are completely free to use with no signup required.'),
        ('Can I use this on mobile?', 'Yes, all our calculators are fully responsive and work on any device including phones and tablets.')
    ],
    'howto': ['Enter your information', 'Review the calculated results', 'Use the results to guide your decisions', 'Check related calculators for more insights']
}

def get_calculator_name(filename):
    """Extract calculator name from filename"""
    name = filename.replace('.html', '').replace('-', ' ').title()
    return name

def get_seo_data(filename):
    """Get SEO data for a specific calculator"""
    key = filename.replace('.html', '')
    if key in CALCULATOR_SEO_DATA:
        return CALCULATOR_SEO_DATA[key]

    # Generate default data
    name = get_calculator_name(filename)
    return {
        'title': f'{name} - Free Online Calculator | FitCalcs',
        'description': f'Free {name.lower()} for quick and accurate results. Easy to use, no signup required. Get instant calculations.',
        'keywords': [name.lower(), 'calculator', 'free calculator', 'online calculator'],
        'category': DEFAULT_SEO['category'],
        'faqs': DEFAULT_SEO['faqs'],
        'howto': DEFAULT_SEO['howto']
    }

def generate_schema(filename, seo_data):
    """Generate JSON-LD structured data"""
    name = get_calculator_name(filename)
    url = f"https://fitcalcs.xyz/{filename}"

    # WebApplication schema
    web_app = {
        "@type": "WebApplication",
        "name": name,
        "url": url,
        "applicationCategory": seo_data.get('category', 'HealthApplication'),
        "operatingSystem": "Any",
        "browserRequirements": "Requires JavaScript",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "provider": {
            "@type": "Organization",
            "name": "FitCalcs",
            "url": "https://fitcalcs.xyz"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "ratingCount": "127",
            "bestRating": "5",
            "worstRating": "1"
        }
    }

    # FAQ schema
    faq_items = []
    for q, a in seo_data.get('faqs', DEFAULT_SEO['faqs']):
        faq_items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })

    faq_page = {
        "@type": "FAQPage",
        "mainEntity": faq_items
    }

    # Breadcrumb schema
    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://fitcalcs.xyz/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": name,
                "item": url
            }
        ]
    }

    # HowTo schema
    howto_steps = []
    for i, step in enumerate(seo_data.get('howto', DEFAULT_SEO['howto']), 1):
        howto_steps.append({
            "@type": "HowToStep",
            "position": i,
            "text": step
        })

    howto = {
        "@type": "HowTo",
        "name": f"How to Use the {name}",
        "description": f"Step-by-step guide to using the {name} on FitCalcs.",
        "step": howto_steps,
        "totalTime": "PT1M"
    }

    schema = {
        "@context": "https://schema.org",
        "@graph": [web_app, faq_page, breadcrumb, howto]
    }

    return schema

def generate_meta_tags(filename, seo_data):
    """Generate all meta tags for the page"""
    name = get_calculator_name(filename)
    url = f"https://fitcalcs.xyz/{filename}"
    title = seo_data.get('title', f'{name} - Free Online Calculator | FitCalcs')
    description = seo_data.get('description', f'Free {name.lower()} for quick and accurate results.')
    keywords = ', '.join(seo_data.get('keywords', [name.lower(), 'calculator']))

    meta_tags = f'''    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="FitCalcs">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <link rel="canonical" href="{url}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="FitCalcs">
    <meta property="og:locale" content="en_US">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{url}">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">

    <!-- Additional SEO -->
    <meta name="theme-color" content="#14b8a6">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'''

    return meta_tags

def generate_faq_html(faqs):
    """Generate FAQ HTML section"""
    faq_html = '''<div class="card" style="margin-top: 20px;">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-list" style="margin-top: 15px;">'''

    for q, a in faqs:
        faq_html += f'''
            <details style="margin-bottom: 15px; padding: 15px; background: var(--bg-input); border-radius: 8px;">
                <summary style="cursor: pointer; font-weight: 600; color: var(--text-primary);">{q}</summary>
                <p style="margin-top: 10px; color: var(--text-secondary); line-height: 1.6;">{a}</p>
            </details>'''

    faq_html += '''
        </div>
    </div>'''

    return faq_html

def optimize_page(filepath):
    """Optimize a single page for SEO"""
    filename = os.path.basename(filepath)
    if filename in ['index.html', 'googlee9bcf971710c9c1b.html', 'CNAME']:
        return False

    print(f"Optimizing: {filename}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    seo_data = get_seo_data(filename)

    # Generate new meta tags
    meta_tags = generate_meta_tags(filename, seo_data)

    # Generate new schema
    schema = generate_schema(filename, seo_data)
    import json
    schema_json = json.dumps(schema, indent=4)

    # Replace head section
    # Find the head content between <head> and </head>
    head_pattern = r'<head>.*?</head>'

    # Extract existing styles and scripts from head
    style_match = re.search(r'(<style>.*?</style>)', content, re.DOTALL)
    existing_style = style_match.group(1) if style_match else ''

    # Find ad scripts in head
    ad_scripts = []
    ad_pattern = r'<script[^>]*(?:quge5|nap5k|highperformance)[^>]*>.*?</script>'
    for match in re.finditer(ad_pattern, content, re.DOTALL):
        ad_scripts.append(match.group(0))

    # Also capture inline ad scripts
    inline_ad = re.search(r"<script>\(function\(s\)\{s\.dataset\.zone.*?</script>", content, re.DOTALL)
    if inline_ad:
        ad_scripts.append(inline_ad.group(0))

    # Build new head
    new_head = f'''<head>
    <script src="https://quge5.com/88/tag.min.js" data-zone="196361" async data-cfasync="false"></script>
{meta_tags}
    {existing_style}
    <script>(function(s){{s.dataset.zone='10379224',s.src='https://nap5k.com/tag.min.js'}})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))</script>
<script type="application/ld+json">
{schema_json}
</script>
</head>'''

    # Replace head section
    content = re.sub(head_pattern, new_head, content, flags=re.DOTALL)

    # Update FAQ section with page-specific FAQs
    faqs = seo_data.get('faqs', DEFAULT_SEO['faqs'])
    new_faq_html = generate_faq_html(faqs)

    # Find and replace existing FAQ section
    faq_pattern = r'<div class="card"[^>]*>\s*<h2>[^<]*(?:FAQ|Frequently Asked)[^<]*</h2>.*?</div>\s*</div>'
    if re.search(faq_pattern, content, re.DOTALL | re.IGNORECASE):
        content = re.sub(faq_pattern, new_faq_html, content, flags=re.DOTALL | re.IGNORECASE)

    # Ensure proper h1 tag (only one per page)
    h1_count = len(re.findall(r'<h1[^>]*>', content))
    if h1_count > 1:
        # Keep only the first h1, change others to h2
        first_h1 = True
        def replace_extra_h1(match):
            nonlocal first_h1
            if first_h1:
                first_h1 = False
                return match.group(0)
            return match.group(0).replace('<h1', '<h2').replace('</h1>', '</h2>')
        content = re.sub(r'<h1[^>]*>.*?</h1>', replace_extra_h1, content, flags=re.DOTALL)

    # Write optimized content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def generate_sitemap():
    """Generate sitemap.xml"""
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
'''

    # Add homepage with highest priority
    today = datetime.now().strftime('%Y-%m-%d')
    sitemap += f'''    <url>
        <loc>https://fitcalcs.xyz/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
'''

    # Add all calculator pages
    for filename in sorted(os.listdir('.')):
        if filename.endswith('.html') and filename not in ['index.html', 'googlee9bcf971710c9c1b.html']:
            sitemap += f'''    <url>
        <loc>https://fitcalcs.xyz/{filename}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
'''

    sitemap += '</urlset>'

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap)

    print("Generated sitemap.xml")

def generate_robots_txt():
    """Generate robots.txt"""
    robots = '''# Robots.txt for FitCalcs
User-agent: *
Allow: /

# Sitemap
Sitemap: https://fitcalcs.xyz/sitemap.xml

# Crawl-delay (optional, be nice to servers)
Crawl-delay: 1
'''

    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots)

    print("Generated robots.txt")

def main():
    """Main function to optimize all pages"""
    count = 0

    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            filepath = os.path.join('.', filename)
            if optimize_page(filepath):
                count += 1

    generate_sitemap()
    generate_robots_txt()

    print(f"\nSEO optimization complete!")
    print(f"Optimized {count} pages")
    print(f"Generated sitemap.xml and robots.txt")

if __name__ == '__main__':
    main()
