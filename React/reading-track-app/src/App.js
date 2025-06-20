import React, {useState, useEffect} from "react";
import api from "./api"

const App = () => {
  const [wishlist, setWishlist] = useState([]);
  const [formData, setFormData] = useState({
    "title": "",
    "author": "",
    "date_added": "",
    "already_own": false
  });

  const fetchWishlist = async () => {
    const response = await api.get("/wishlist")
    
    setWishlist(response.data)
  };

  useEffect(() => {
    fetchWishlist();
  }, [])

  const handleInputChange = (event) => {
    const value = event.target.type === "checkbox" ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };


  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post("/wishlist", formData);
    fetchWishlist();
    setFormData({
      "title": "",
      "author": "",
      "date_added": "",
      "already_own": false
    });
   };


  return(
    <div>
      <nav className="navbar navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            ReadTrak
          </a>
        </div>
      </nav>

      <div className="container">
        <form onSubmit={handleFormSubmit}>

          <div className="mb-3 mt-3">
            <label htmlFor="title" className="form-label">
              Title
            </label>
            <input type="text" className="form-control" id="title" name="title" onChange={handleInputChange} placeholder="Moby Dick" value={formData.title}/>
          </div>

          <div className="mb-3">
            <label htmlFor="author" className="form-label">
              Author
            </label>
            <input type="text" className="form-control" id="author" name="author" onChange={handleInputChange} placeholder="Herman Melville" value={formData.author}/>
          </div>

          <div className="mb-3">
            <label htmlFor="date_added" className="form-label">
              Date Added
            </label>
            <input type="text" className="form-control" id="date_added" name="date_added" onChange={handleInputChange} placeholder="YYYY-MM-DD" value={formData.date_added}/>
          </div>

          <div className="mb-3">
            <label htmlFor="already_own" className="form-label">
              Already Own?
            </label>
            <input type="checkbox" id="already_own" name="already_own" onChange={handleInputChange} value={formData.already_own}/>
          </div>

          <button type="submit" className="btn btn-primary mb-3">
            Add Book
          </button>

        </form>

        <table className="table table-striped table-bordered table-hover">
          <thead>

            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>Date Added</th>
              <th>Already Own</th>
            </tr>

          </thead>

          <tbody>
            {wishlist.map((wishlist) => (
              <tr key={wishlist.id}>
                <td>{wishlist.title}</td>
                <td>{wishlist.author}</td>
                <td>{wishlist.date_added}</td>
                <td>{wishlist.already_own ? "Owned" : "Not Owned"}</td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

      
    </div>
  )
}

export default App;
