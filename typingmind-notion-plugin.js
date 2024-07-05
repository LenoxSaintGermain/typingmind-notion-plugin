typingmind.plugin({
    name: "Notion Database Updater",
    actions: {
        "updateNotionDatabase": async ({ payload }) => {
            try {
                const { llmOutput, notes } = payload; 
                const apiKey = typingmind.user.getSetting('notionApiKey'); 
                const databaseId = typingmind.user.getSetting('notionDatabaseId');

                const formattedData = formatDataForNotion(llmOutput, notes);

                // Since we can't directly use the Notion API in the browser,
                // we'll need to send this data to our server
                const response = await fetch('https://your-render-app-url.com/update-notion', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        apiKey,
                        databaseId,
                        formattedData
                    }),
                });

                const result = await response.json();

                if (result.success) {
                    console.log("Page created successfully:", result.pageId);
                    // Optionally: Display a success message to the user
                } else {
                    console.error("Error creating page:", result.error);
                    // Optionally: Display an error message to the user
                }
            } catch (error) {
                console.error("Plugin error:", error);
                // Optionally: Display an error message to the user
            }
        }
    }
});

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