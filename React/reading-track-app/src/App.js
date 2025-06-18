import React, {useState, useEffect} from "react";
import api from "./api"

const App = () => {
  const [wishlist, setWishlist] = useState([]);
  const [formData, setFormData] = useState({
    "title": "",
    "author": "",
    "date": "",
  });

  const fetchWishlist = async () => {
    const response = await api.get("/wishlist")
    
    setWishlist(response.data)
  };

  useEffect(() => {
    fetchWishlist();
  }, [])

  // const handleInputChange = (event) => {
  //   const value = event.target.type === "checkbox" ? event.target.checked : event.target.value;
  //   setFormData({
  //     [event.target.name]: value,
  //   });
  // };


  // const handleFormSubmit = async (event) => {
  //   event.preventDefault();
  //   await api.post("/wishlist", formData);
  //   fetchWishlist();
  //   setFormData({
  //     "title": "",
  //     "author": "",
  //     "date": "",
  //   });
  //  };


  return(
    <div>
      <nav className="navbar navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            ReadTrak
          </a>

        </div>
      </nav>
    </div>
  )
}

export default App;
