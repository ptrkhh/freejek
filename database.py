from supabase import create_client

from backend.entities.schema_public_latest import VehicleModel, VehicleModelBaseSchema

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("KESINI0")
new_vehicle_model = VehicleModelBaseSchema(
    make="Daihatsu",
    model="Sigra",
    propulsion="petrol",
    type="car",
    vehicle_class=1,
    capacity=7,
)
print("KESINI1")
supabase.table("vehicle_model").insert(new_vehicle_model.model_dump(exclude={"id", "created_at"})).execute()

print("KESINI2")
