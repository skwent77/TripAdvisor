 import useFetch from "../hooks/loadData.jsx";

export async function CreateForm(formData) {
    try {

        // you need to doublecheck for posting to form and then get response from same api form
        // THE TRIP COURSE IS GETTING RESPONSE DATA FROM TEMPORAL JSON DATA CALLED 'https://api.visit-with-tripper.site/PlanData'
        // DO NOT FORGET TO CHANGE PlanData API FROM MainContent.jsx
        const formResponse = await fetch(`https://api.visit-with-tripper.site/api/v1/plans`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...formData
            }),
        });

        if (!formResponse.ok) {
            alert('Failed to post new form');
            return; // Stop execution if the form POST fails
        }

        alert("New chat and form created successfully!");
        return {
            PlanData: await formResponse.json(),
        };

    } catch (error) {
        console.error("Error in CreateForm:", error);
        alert("Failed to create new chat and form.");
        throw error;
    }
}