import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: false,
    headers: {
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS'
    }
});

export default api;