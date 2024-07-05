import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from notion_client import Client

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

def format_data_for_notion(llm_output, notes=""):
    property_mapping = {
        "Company Name": "Company Name",
        "Website": "Website",
        "Location": "Location",
        "Industry": "Industry",
        "Year Founded": "Year founded",
        "Description": "Company Description",
        "Business Model": "Business Model / Revenue Streams:",
        "Product": "What the product is/products",
        "Revenue": "Traction/revenue as available",
        "Competitors": "Competitors & Competitive Advantages:",
        "Management": "Management Team & Background:",
        "Funding History": "Fundraising History",
        "VC Backed": "VC / PE backed",
        "Deal Stage": "Deal Stage",
        "Deal Size": "Deal Size",
        "Technology": "Innovative Technology ",
        "Target Customer": "Target Customer Profile ",
        "Features": "Main Features",
        "Address": "Address",
        "Contact Name": "Contact Name",
        "Contact Email": "Contact Email",
        "Founder's Link": "Founder's Link",
        "Other Link": "Other Link (Pitchbook, Tracxn, etc.)",
        "Funding Stage": "Funding Stage",
        "Post Valuation": "Post Valuation",
        "Funding to Date": "Funding to Date",
        "Target Close": "Target Close",
        "Deal Type": "Deal Type",
        "Notable Partnerships": "Notable Partnership / Clients / Suppliers",
        "Deal Source": "Deal Source",
        "Person in Charge": "Person-in-charge",
        "Investors Interested": "Investors Interested"
    }

    formatted_data = {}
    for llm_key, notion_property in property_mapping.items():
        if llm_key in llm_output:
            value = llm_output[llm_key]
            if notion_property == "Company Name":
                formatted_data[notion_property] = {"title": [{"text": {"content": str(value)}}]}
            elif notion_property == "Industry":
                formatted_data[notion_property] = {"multi_select": [{"name": value}]}
            elif notion_property in ["Deal Stage", "Funding Stage"]:
                formatted_data[notion_property] = {"select": {"name": value}}
            elif notion_property in ["Website", "Founder's Link", "Other Link (Pitchbook, Tracxn, etc.)"]:
                formatted_data[notion_property] = {"url": value if value.startswith("http") else f"https://{value}"}
            elif notion_property in ["Deal Size", "Post Valuation", "Funding to Date"]:
                formatted_data[notion_property] = {"number": float(value.replace("$", "").replace(",", "")) if value else None}
            elif notion_property == "Target Close":
                formatted_data[notion_property] = {"date": {"start": value}}
            elif notion_property == "Contact Email":
                formatted_data[notion_property] = {"email": value}
            elif notion_property == "Deal Type":
                formatted_data[notion_property] = {"multi_select": [{"name": value}]}
            elif notion_property in ["Deal Source", "Person-in-charge"]:
                formatted_data[notion_property] = {"people": []}
            elif notion_property == "Investors Interested":
                formatted_data[notion_property] = {"relation": []}
            else:
                formatted_data[notion_property] = {"rich_text": [{"text": {"content": str(value)}}]}

    if notes:
        formatted_data["Meeting Notes/Record"] = {"url": notes if notes.startswith("http") else "https://example.com"}

    return formatted_data

def update_notion_database(api_key, database_id, formatted_data):
    try:
        notion = Client(auth=api_key)
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=formatted_data
        )
        print(f"Successfully added new page to Notion. Page ID: {response['id']}")
        return True, response['id']
    except Exception as e:
        print(f"Error updating Notion database: {str(e)}")
        return False, str(e)

@app.route("/update-notion", methods=['POST'])
def update_notion():
    try:
        data = request.json
        api_key = data.get('apiKey', os.environ['NOTION_API_KEY'])
        database_id = data.get('databaseId', os.environ['NOTION_DATABASE_ID'])
        llm_output = data.get('llmOutput', {})
        notes = data.get('notes', '')

        formatted_data = format_data_for_notion(llm_output, notes)
        success, result = update_notion_database(api_key, database_id, formatted_data)

        if success:
            return jsonify({"success": True, "pageId": result})
        else:
            return jsonify({"success": False, "error": result})

    except Exception as error:
        print('Error:', error)
        return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 3000)))