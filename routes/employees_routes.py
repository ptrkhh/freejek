from fastapi import APIRouter, Request, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import SUPABASE_KEY
from ..database import supabase

router = APIRouter()
templates = Jinja2Templates(directory="./employee_repo/templates")


@router.get("/", response_class=HTMLResponse)
async def read_employees(request: Request):
    response = supabase.table('employees').select('*').eq('is_active', True).execute()
    employees = response.data
    return templates.TemplateResponse('index.html', {"request": request, "employees": employees})


@router.get("/add", response_class=HTMLResponse)
async def add_employee_form(request: Request):
    return templates.TemplateResponse("add_employees.html", {"request": request})

@router.post("/add")
async def add_employee(request: Request, employee: EmployeeCreate = Depends(EmployeeCreate.as_form), image: UploadFile = File(None)):
    image_url = None
    if image and image.filename:
        image_filename = f"{employee.first_name}_{employee.last_name}_{image.filename}"
        file_content = await image.read()
        response = supabase.storage.from_(SUPABASE_BUCKET).upload(image_filename, file_content)
        image_url = image.filename
