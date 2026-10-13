import apiClient from "./api"

// Function to check the server status
export default async function serverStatus(): Promise<boolean> {
    try {
        const serverStats = await apiClient.get("/");
        if (serverStats?.data?.success) {
            return true
        }
        else {
            return false
        }
    }
    catch(err){
        console.log(err);
        return false;
    }
}