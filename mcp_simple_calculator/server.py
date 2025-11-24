from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

# Create FastAPI app instance
app = FastAPI(
    title="Simple Calculator API",
    description="A simple calculator MCP server",
    version="1.0.0"
)

# Request models
class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

# Calculator functions
def add_numbers(a: float, b: float) -> float:
    return a + b

def multiply_numbers(a: float, b: float) -> float:
    return a * b

def subtract_numbers(a: float, b: float) -> float:
    return a - b

def divide_numbers(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# API Routes
@app.get("/")
async def root():
    return {
        "message": "Simple Calculator MCP Server", 
        "version": "1.0.0",
        "endpoints": [
            "/tools",
            "/calculate",
            "/docs"
        ]
    }

@app.get("/tools")
async def list_tools() -> List[ToolDefinition]:
    """List all available calculator tools"""
    return [  
        ToolDefinition(
            name="add",
            description="Add two numbers together",
            parameters={
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            }
        ),
        ToolDefinition(
            name="multiply",
            description="Multiply two numbers together",
            parameters={
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            }
        ),
        ToolDefinition(
            name="subtract",
            description="Subtract the second number from the first",
            parameters={
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            }
        ),
        ToolDefinition(
            name="divide",
            description="Divide the first number by the second",
            parameters={
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number (non-zero)"}
            }
        )
    ]

@app.post("/calculate")
async def calculate(request: CalculationRequest):
    """Perform a calculation operation"""
    try:
        if request.operation == "add":
            result = add_numbers(request.a, request.b)
            return {
                "operation": "add",
                "expression": f"{request.a} + {request.b}",
                "result": result,
                "success": True
            }
        elif request.operation == "multiply":
            result = multiply_numbers(request.a, request.b)
            return {
                "operation": "multiply",
                "expression": f"{request.a} × {request.b}",
                "result": result,
                "success": True
            }
        elif request.operation == "subtract":
            result = subtract_numbers(request.a, request.b)
            return {
                "operation": "subtract",
                "expression": f"{request.a} - {request.b}",
                "result": result,
                "success": True
            }
        elif request.operation == "divide":
            result = divide_numbers(request.a, request.b)
            return {
                "operation": "divide",
                "expression": f"{request.a} ÷ {request.b}",
                "result": result,
                "success": True
            }
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown operation: {request.operation}. Available operations: add, multiply, subtract, divide"
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "calculator-api"}

# Quick calculation endpoints for simple GET requests
@app.get("/add")
async def add_get(a: float, b: float):
    """Add two numbers via GET request"""
    result = add_numbers(a, b)
    return {"operation": "add", "result": result, "expression": f"{a} + {b}"}

@app.get("/multiply")
async def multiply_get(a: float, b: float):
    """Multiply two numbers via GET request"""
    result = multiply_numbers(a, b)
    return {"operation": "multiply", "result": result, "expression": f"{a} × {b}"}

@app.get("/subtract")
async def subtract_get(a: float, b: float):
    """Subtract two numbers via GET request"""
    result = subtract_numbers(a, b)
    return {"operation": "subtract", "result": result, "expression": f"{a} - {b}"}

# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )