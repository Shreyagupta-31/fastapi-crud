from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# FastAPI app is working. Run this file and open http://127.0.0.1:8000 in the browser.

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

app = FastAPI(title="FastAPI Example", version="1.0.0")

# In-memory product storage
products_db = {
    1: Product(id=1, name="Laptop", description="High-performance laptop", price=999.99, quantity=5),
    2: Product(id=2, name="Mouse", description="Wireless mouse", price=29.99, quantity=50),
    3: Product(id=3, name="Keyboard", description="Mechanical keyboard", price=89.99, quantity=20),
}

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running and working", "version": "1.0.0"}

@app.get("/products", response_model=List[Product])
async def list_products():
    """Get all products"""
    return list(products_db.values())

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get a specific product by ID"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

@app.post("/products", response_model=Product)
async def create_product(product: Product):
    """Create a new product"""
    if product.id in products_db:
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products_db[product.id] = product
    return product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    """Update an existing product"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db[product_id] = product
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    """Delete a product"""
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"message": f"Product {product_id} deleted successfully"}

@app.get("/status")
async def app_status():
    """Get app status and stats"""
    return {
        "status": "running",
        "total_products": len(products_db),
        "endpoint": "http://127.0.0.1:8000"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
