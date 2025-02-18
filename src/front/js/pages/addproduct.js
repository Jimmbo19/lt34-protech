import React, { useState, useEffect, useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";
import "/workspaces/lt34-protech/src/front/styles/addproduct.css";

export const AddProduct = () => {
	const { store, actions } = useContext(Context);
	const [name,setName] = useState("")
	const [description,setDescription] = useState("")
	const [price,setPrice] = useState(0)
	const [stock,setStock] = useState(0)
	const [categories,setCategories] = useState([])
	const [categoryId,setCategoryId] = useState(0)
	const [imageProduct,setImageProduct] = useState("")
	const navigate = useNavigate();

	const cloudName = "dqs1ls601";
  	const presetName = "Protech";


	const getCategories = () => {
		const token = actions.verifyTokenSeller();

		fetch(`${process.env.BACKEND_URL}/api/categorias`, {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error("Error fetching products: " + response.statusText);
				}
				return response.json();
			})
			.then((data) => {
				setCategories(data)
                
			})
			.catch((error) => {
				console.error("Error fetching cart items:", error);
			});
	};

	useEffect(() => {
		getCategories()
	}, []);

	const createProduct = (e) =>{
		e.preventDefault();
		
		const raw = JSON.stringify({
			name: name,
			description: description,
			price: parseInt(price),
			stock: parseInt(stock),
			image: imageProduct,
			category_id: categoryId
		});

		const token = actions.verifyTokenSeller();

		if (!token) {
		console.error("No valid token found. User might need to log in.");
		return;
		}

		fetch(`${process.env.BACKEND_URL}/api/products`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"Authorization": `Bearer ${token}`
			},
			body: raw
		})
		.then(() => {
			cleanFields();
			navigate("/dashboard/products")
		})
		.catch((error) => console.error("Error creating product:", error));
	}
	const handleFileChange = async (e) => {
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append("file", file);
        formData.append("upload_preset", presetName);
    
        try {
            const response = await fetch(`https://api.cloudinary.com/v1_1/${cloudName}/image/upload`, {
                method: "POST",
                body: formData
            });
    
            const data = await response.json();
            const imageUrl = data.secure_url;

            setImageProduct(imageUrl)
            
        } catch (error) {
            console.error("Error uploading image:", error);
        }
    };
	const cleanFields = () =>{
		setName("")
		setDescription("")
		setPrice(0)
		setStock(0)
		setImageProduct("")
		
	}

	return (
		<div style={{ paddingBottom: "100px" }}>
			<div className="row mb-5" >
				<div className="col-12 d-flex">
					<div>
						<h2>Add New Product</h2>
					</div>
					<div className="ms-auto mt-5">
						<button className="purple-button" onClick={() => navigate("/dashboard/products")}>Back to products</button>
					</div>
				</div>
			</div>
			<div className="row">
				<div className="col-12">
					<div className="card-black body-card">
						<h5 className="mb-4">Product Information</h5>
						<form onSubmit={()=>createProduct()}>
							<div className="row mb-3">
								<div className="col-6">
									<label htmlFor="name">Title</label>
									<input id="name" value={name} onChange={(e)=>setName(e.target.value)} placeholder="Product name" className="form-control" type="text" required></input>
								</div>
								<div className="col-6">
									<label htmlFor="category">Product category</label>
									<select value={categoryId || ""} onChange={(e) => setCategoryId(Number(e.target.value))} className="form-select" id="category">
										<option value="" disabled>Select Category</option> 
										{categories.length > 0 ? (
											categories.map((category) => (
											<option key={category.id} value={category.id}>{category.name}</option>
											))
										) : <></>}
									</select>
								</div>
							</div>
							<div className="row mb-3">
								<div className="col-6">
									<label htmlFor="price">Price</label>
									<input
										className="form-control" id="price"
										value={price} onChange={(e)=>setPrice(e.target.value)} 
										placeholder="Product price" type="number" required
									></input>
								</div>
								<div className="col-6">
									<label htmlFor="stock">Stock</label>
									<input 
										className="form-control" id="stock" 
										value={stock} onChange={(e)=>setStock(e.target.value)}
										placeholder="Product stock" type="number" required
								></input>
								</div>
							</div>
							<div className="row">
								<div className="col-12">
									<div className="mb-3">
										<label htmlFor="formFile" className="form-label">Product Image</label>
										<input 
											type="file"
											accept="image/*" id="formFile"
											onChange={(e)=>handleFileChange(e)}  />
									</div>
								</div>
							</div>
							<div className="row">
								<div className="col-12">
									<div className="mb-3">
										<label htmlFor="description" className="form-label">Product Descriptions</label>
										<textarea 
											className="form-control" id="description" 
											value={description} onChange={(e)=>setDescription(e.target.value)} 
											rows="3" maxLength={900}
										></textarea>
									</div>
								</div>
							</div>
							<div className="row">
								<div className="col-12 d-flex">
									<div className="mb-3 ms-auto">
										<button className="purple-button" type="submit" onClick={createProduct}>Create</button>
									</div>
								</div>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	);
};