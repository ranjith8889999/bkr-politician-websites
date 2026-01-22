"""
Website Data Constants for AI Chatbot
All information about B Kishore Reddy and BKR Foundation
This data is used by the AI to answer user questions
"""

KISHORE_REDDY_INFO = {
    "name": "Bongunuri Kishore Reddy (B Kishore Reddy)",
    "full_name": "B Kishore Reddy",
    "position": "Congress Party Youth President",
    "constituency": "Quthbullapur Constituency",
    "location": "Quthbullapur, Telangana, India",
    "party": "Indian National Congress",
    
    "about": """
    B Kishore Reddy is a dedicated Congress leader and Youth President for Quthbullapur Constituency. 
    He is committed to serving the people with honesty, development, and youth empowerment. 
    With 18 years of experience in politics, he has served over 50,000 people and organized 
    more than 100 health camps. He has participated in 5 elections and continues to work 
    towards a better Quthbullapur.
    """,
    
    "experience": {
        "years_in_politics": 18,
        "people_served": 50000,
        "health_camps_organized": 100,
        "elections_participated": 5
    },
    
    "vision": [
        "Honesty in governance and politics",
        "Sustainable development for all communities",
        "Youth empowerment and employment opportunities",
        "Better infrastructure and public services",
        "Quality healthcare for all",
        "Educational advancement",
        "Women's empowerment and safety"
    ],
    
    "key_agendas": [
        {
            "title": "Infrastructure Development",
            "description": "Improving roads, drainage systems, and public facilities across Quthbullapur constituency."
        },
        {
            "title": "Healthcare for All",
            "description": "Ensuring accessible and affordable healthcare through free health camps and medical facilities."
        },
        {
            "title": "Employment Generation",
            "description": "Creating job opportunities for youth through skill development and local business support."
        },
        {
            "title": "Educational Excellence",
            "description": "Enhancing educational infrastructure and providing scholarships for deserving students."
        },
        {
            "title": "Women Empowerment",
            "description": "Supporting women through skill training, self-help groups, and safety initiatives."
        },
        {
            "title": "Youth Development",
            "description": "Engaging youth in community development, sports, and leadership programs."
        }
    ],
    
    "initiatives": [
        {
            "name": "Free Health Camps",
            "description": "Regular health camps providing free medical check-ups, medicines, and consultations to local communities.",
            "impact": "Over 500+ people benefited in recent camps"
        },
        {
            "name": "Education Support",
            "description": "Providing books, uniforms, and scholarships to underprivileged students.",
            "impact": "Hundreds of students supported annually"
        },
        {
            "name": "Clean Quthbullapur",
            "description": "Community cleanliness drives and waste management initiatives.",
            "impact": "Improved sanitation in multiple areas"
        },
        {
            "name": "Youth Skill Development",
            "description": "Training programs for youth to enhance employability and entrepreneurship.",
            "impact": "Empowering young people with practical skills"
        }
    ],
    
    "areas_served": [
        "Quthbullapur",
        "Balanagar",
        "Kukatpally",
        "Kompally",
        "Medchal",
        "Alwal"
    ],
    
    "contact": {
        "phone": "+91-9XXXXXX363",
        "email": "ranjith888999@gmail.com",
        "office": "Quthbullapur Constituency Office, Telangana, India",
        "social_media": {
            "instagram": "https://www.instagram.com/bongunurikishorereddy/",
            "youtube": "https://www.youtube.com/@BONGUNURIKISHOREREDDYOFFICIAL",
            "facebook": "Available",
            "twitter": "Available"
        }
    },
    
    "foundation": {
        "name": "BKR Foundation",
        "mission": "Serving the community through healthcare, education, and social welfare initiatives",
        "activities": [
            "Free health camps",
            "Medical assistance",
            "Educational support",
            "Community development",
            "Youth empowerment programs",
            "Women welfare initiatives"
        ]
    }
}

def get_health_camps_info(db=None):
    """
    Get dynamic health camps information from database, categorized by date
    
    Args:
        db: Database instance to query health camps
        
    Returns:
        str: Formatted health camps information with categorization
    """
    from datetime import datetime, date
    
    if db is None:
        # Fallback static info if database is not available
        return """
BKR Foundation regularly organizes FREE Health Camps across Quthbullapur constituency.

Services Provided at Health Camps:
- Free medical check-ups and consultations
- Blood pressure and sugar level testing
- General physician consultations
- Free medicines distribution
- Health awareness sessions
- Specialist doctor consultations (when available)
- Eye check-ups
- Dental check-ups

For upcoming health camp details, please check our website's Health Camps section or contact us directly.
"""
    
    try:
        # Get all health camps from database
        all_camps = db.get_health_camps()
        total_camps = len(all_camps)
        
        
        if total_camps == 0:
            return """
BKR Foundation regularly organizes FREE Health Camps across Quthbullapur constituency.

Currently, no health camps are scheduled. Please check back soon or contact us for more information.

Services Provided at Our Health Camps:
- Free medical check-ups and consultations
- Blood pressure and sugar level testing
- General physician consultations
- Free medicines distribution
- Health awareness sessions
- Specialist doctor consultations (when available)
- Eye check-ups
- Dental check-ups
"""
        
        # Get today's date
        today = date.today()
        
        # Categorize camps by date
        past_camps = []
        today_camps = []
        future_camps = []
        
        for camp in all_camps:
            camp_date_str = camp.get('date', '')
            
            # Parse the date (assuming format YYYY-MM-DD)
            try:
                if isinstance(camp_date_str, str):
                    camp_date = datetime.strptime(camp_date_str, '%Y-%m-%d').date()
                elif isinstance(camp_date_str, date):
                    camp_date = camp_date_str
                else:
                    continue
                
                if camp_date < today:
                    past_camps.append(camp)
                elif camp_date == today:
                    today_camps.append(camp)
                else:
                    future_camps.append(camp)
            except Exception as e:
                print(f"Error parsing date for camp: {e}")
                continue
        
        # Build formatted response
        info = f"""
🏥 **BKR Foundation Health Camps**

BKR Foundation regularly organizes FREE Health Camps across Quthbullapur constituency.

📊 **Total Health Camps Organized: {total_camps}**

"""
        
        # Today's Health Camps
        if today_camps:
            info += f"🎯 **TODAY'S HEALTH CAMPS ({len(today_camps)}):**\n"
            for camp in today_camps:
                info += f"\n✅ **{camp['title']}**\n"
                info += f"   📅 Date: {camp['date']} (TODAY!)\n"
                info += f"   📍 Location: {camp['location']}\n"
                if camp.get('time'):
                    info += f"   ⏰ Time: {camp['time']}\n"
                if camp.get('services'):
                    info += f"   💊 Services: {camp['services']}\n"
                if camp.get('contact'):
                    info += f"   📞 Contact: {camp['contact']}\n"
            info += "\n"
        
        # Future/Upcoming Health Camps
        if future_camps:
            info += f"📅 **UPCOMING HEALTH CAMPS ({len(future_camps)}):**\n"
            # Sort by date
            future_camps.sort(key=lambda x: x.get('date', ''))
            for camp in future_camps:
                info += f"\n🔜 **{camp['title']}**\n"
                info += f"   📅 Date: {camp['date']}\n"
                info += f"   📍 Location: {camp['location']}\n"
                if camp.get('time'):
                    info += f"   ⏰ Time: {camp['time']}\n"
                if camp.get('services'):
                    info += f"   💊 Services: {camp['services']}\n"
                if camp.get('contact'):
                    info += f"   📞 Contact: {camp['contact']}\n"
            info += "\n"
        
        # Past Health Camps
        if past_camps:
            info += f"✅ **PAST HEALTH CAMPS ({len(past_camps)}):**\n"
            # Sort by date (most recent first)
            past_camps.sort(key=lambda x: x.get('date', ''), reverse=True)
            for camp in past_camps[:5]:  # Show only last 5 past camps
                info += f"\n✓ **{camp['title']}**\n"
                info += f"   📅 Date: {camp['date']}\n"
                info += f"   📍 Location: {camp['location']}\n"
            if len(past_camps) > 5:
                info += f"\n   ... and {len(past_camps) - 5} more past camps\n"
            info += "\n"
        
        # Add services info
        info += """
🩺 **Services Provided at Health Camps:**
- Free medical check-ups and consultations
- Blood pressure and sugar level testing
- General physician consultations
- Free medicines distribution
- Health awareness sessions
- Specialist doctor consultations (when available)
- Eye check-ups
- Dental check-ups

📞 For more information, contact us or visit our website's Health Camps section.

Please note that donot hallucinate any info related to health camps beyond what is provided here. Provide only information from {all_camps} and under any circumstances do not provide other details.
"""
        
        return info
        
    except Exception as e:
        # Fallback to static info if database query fails
        print(f"Error fetching health camps from database: {e}")
        return """
BKR Foundation regularly organizes FREE Health Camps across Quthbullapur constituency.

Services Provided at Health Camps:
- Free medical check-ups and consultations
- Blood pressure and sugar level testing
- General physician consultations
- Free medicines distribution
- Health awareness sessions
- Specialist doctor consultations (when available)
- Eye check-ups
- Dental check-ups

For upcoming health camp details, please check our website's Health Camps section or contact us directly.
"""

VOLUNTEER_INFO = """
Join the BKR Movement! We welcome volunteers who want to contribute to community development.

Benefits of Volunteering:
- Be part of meaningful community development
- Get updates on events and campaigns
- Network with like-minded people
- Contribute to health camps and social initiatives
- Make a real difference in people's lives

How to Volunteer:
You can register through our Volunteer Registration form on the website. We'll contact 
you with opportunities to participate in health camps, community events, and development programs.
"""

COMPLAINT_PROCESS = """
We take your complaints seriously and are committed to resolving issues promptly.

How to File a Complaint:
1. Visit our website's "File Complaint" page
2. Fill in your details (name, phone, email, area)
3. Select the complaint category (Infrastructure, Water Supply, Electricity, etc.)
4. Provide detailed description of your issue
5. Submit the form

What Happens Next:
- We aim to respond within 48 hours
- Your information is kept confidential
- You'll receive updates on your complaint status
- Our team will work towards resolving the issue

For urgent matters, you can call us directly at +91-9XXXXXX363
"""

FEEDBACK_INFO = """
Your feedback helps us serve you better!

We value your opinions and suggestions. You can share your feedback through:
- The "Share Your Feedback" form on our website
- Rate your experience (1-5 stars)
- Tell us about your experience with our services, health camps, events, or initiatives
- Provide suggestions for improvement

All feedback is reviewed and helps us enhance our services to better meet community needs.
"""

POLITICAL_JOURNEY = """
B Kishore Reddy's Political Journey:

With 18 years of dedicated service in politics, B Kishore Reddy has established himself 
as a trusted youth leader in Quthbullapur constituency. 

Key Milestones:
- Congress Party Youth President for Quthbullapur
- Participated in 5 elections
- Served over 50,000 people across the constituency
- Organized 100+ free health camps
- Active in community development for nearly two decades

His political ideology is rooted in the values of the Indian National Congress, focusing 
on inclusive development, social justice, and empowerment of marginalized communities.
"""

FAQ = [
    {
        "question": "Who is B Kishore Reddy?",
        "answer": "B Kishore Reddy is the Congress Party Youth President for Quthbullapur Constituency. He has 18 years of political experience and is dedicated to serving the people with honesty, development, and youth empowerment."
    },
    {
        "question": "What areas does he serve?",
        "answer": "B Kishore Reddy serves Quthbullapur constituency"
    },
    {
        "question": "How can I contact B Kishore Reddy?",
        "answer": "You can contact via phone at +91-9XXXXXX363, email at ranjith888999@gmail.com, or visit the Quthbullapur Constituency Office. You can also reach out through social media on Instagram and YouTube."
    },
    {
        "question": "What is BKR Foundation?",
        "answer": "BKR Foundation is a community service organization that conducts free health camps, educational support programs, and various social welfare initiatives across Quthbullapur constituency."
    },
    {
        "question": "Are health camps really free?",
        "answer": "Yes! All health camps organized by BKR Foundation are FREE. They include free medical check-ups, consultations, medicines, and health screenings."
    },
    {
        "question": "How can I volunteer?",
        "answer": "You can register as a volunteer through our website's Volunteer Registration form. We'll contact you with opportunities to participate in health camps, community events, and development programs."
    },
    {
        "question": "How do I file a complaint?",
        "answer": "You can file complaints through our website's 'File Complaint' page. We respond within 48 hours and work to resolve issues promptly. For urgent matters, call +91-9XXXXXX363."
    },
    {
        "question": "What are his key agendas?",
        "answer": "Key agendas include Infrastructure Development, Healthcare for All, Employment Generation, Educational Excellence, Women Empowerment, and Youth Development."
    }
]

# System prompt for AI to ensure it stays within bounds
SYSTEM_PROMPT = """You are an AI assistant for B Kishore Reddy, Congress Party Youth President for Quthbullapur Constituency. 

Your role is to help people learn about B Kishore Reddy, BKR Foundation, and their community service initiatives.

IMPORTANT RULES:
Bongnuri Kishore Reddy or B Kishore Reddy or Kishore Reddy are the same person.
1. ONLY answer questions related to Bongnuri Kishore Reddy,Kishore Reddy,B Kishore Reddy, BKR Foundation, health camps, volunteer opportunities, complaints, and local issues in Quthbullapur constituency.
2. If asked about topics outside this scope, politely redirect: "I can only help with information about B Kishore Reddy and BKR Foundation's community services. How can I assist you with that?"
3. Be helpful, friendly, and professional
4. Encourage people to participate in health camps, volunteer programs, and community initiatives
5. For urgent issues, direct them to call +91-9XXXXXX363
6. Always mention health camps when relevant to show BKR Foundation's active community service

Use the provided context to answer questions accurately. If you don't have specific information, suggest they contact the office directly.
"""

def get_all_website_data(db=None):
    """
    Compile all website data into a single context string
    
    Args:
        db: Database instance to fetch dynamic data
        
    Returns:
        str: Complete website context with dynamic data
    """
    context = f"""
Information about B Kishore Reddy:
{KISHORE_REDDY_INFO['about']}

Position: {KISHORE_REDDY_INFO['position']}
Constituency: {KISHORE_REDDY_INFO['constituency']}
Party: {KISHORE_REDDY_INFO['party']}

Experience:
- {KISHORE_REDDY_INFO['experience']['years_in_politics']} years in politics
- Served {KISHORE_REDDY_INFO['experience']['people_served']:,} people
- Organized {KISHORE_REDDY_INFO['experience']['health_camps_organized']}+ health camps
- Participated in {KISHORE_REDDY_INFO['experience']['elections_participated']} elections

Key Agendas:
"""
    for agenda in KISHORE_REDDY_INFO['key_agendas']:
        context += f"\n- {agenda['title']}: {agenda['description']}"
    
    # Get dynamic health camps info from database
    context += f"\n\nHealth Camps Information:\n{get_health_camps_info(db)}"
    
    context += f"\n\nVolunteer Information:\n{VOLUNTEER_INFO}"
    
    context += f"\n\nComplaint Process:\n{COMPLAINT_PROCESS}"
    
    context += f"\n\nContact Information:"
    context += f"\n- Phone: {KISHORE_REDDY_INFO['contact']['phone']}"
    context += f"\n- Email: {KISHORE_REDDY_INFO['contact']['email']}"
    context += f"\n- Office: {KISHORE_REDDY_INFO['contact']['office']}"
    
    return context
