import csv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

ADDRESS_DATABASE_URL = "sqlite:///./address.db"
address_engine = create_engine(ADDRESS_DATABASE_URL, connect_args={"check_same_thread": False})
AddressSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=address_engine)
AddressBase = declarative_base()

class Address(AddressBase):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    province = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    used_by = Column(String, nullable=True)

AddressBase.metadata.create_all(bind=address_engine)

def import_addresses_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Detected CSV headers:", reader.fieldnames)
        # Normalize headers to lowercase, strip spaces, and remove BOM if present
        field_map = {k.strip().lower().replace('\ufeff', ''): k for k in reader.fieldnames}
        required = ['street', 'city', 'province', 'zip']
        for req in required:
            if req not in field_map:
                raise Exception(f"CSV is missing required column: {req}")
        session = AddressSessionLocal()
        addresses = []
        for row in reader:
            address = Address(
                street=row[field_map['street']].strip(),
                city=row[field_map['city']].strip(),
                province=row[field_map['province']].strip(),
                zip=row[field_map['zip']].strip(),
                used=False,
                used_at=None,
                used_by=None
            )
            addresses.append(address)
        session.bulk_save_objects(addresses)
        session.commit()
        session.close()
        print(f"{len(addresses)} addresses imported successfully.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python import_addresses.py <csv_file_path>")
    else:
        import_addresses_from_csv(sys.argv[1])
