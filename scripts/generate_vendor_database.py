import random
import pandas as pd

print("RUNNING NEW VENDOR GENERATOR V2")
# ==============================================
# LOAD EQUIPMENT MASTER
# ==============================================

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

vendor_records = []

vendor_counter = 1

# ==============================================
# VENDOR MAPPING
# ==============================================

VENDOR_MAP = {

    "Vehicle":[
        "Tata Motors",
        "Ashok Leyland",
        "BharatBenz",
        "Mahindra Truck",
        "Force Motors"
    ],

    "Mechanical":[
        "JCB India",
        "BEML",
        "CASE India",
        "ACE",
        "Kirloskar",
        "Crompton",
        "KSB Pumps"
    ],

    "Electronic":[
        "Siemens",
        "ABB",
        "Honeywell",
        "Bosch",
        "Schneider Electric",
        "L&T"
    ],

    "Static":[
        "Nilkamal",
        "Supreme",
        "Sintex",
        "Prince Pipes"
    ],

    "Manual":[
        "Safari Industries",
        "Supreme",
        "Nilkamal"
    ]

}

# ==============================================
# SPECIFICATION LIBRARY
# ==============================================

SPECIFICATIONS = {

"Garbage Compactor Truck":[
"14 Cu.m BS-VI Hydraulic Compactor",
"16 Cu.m BS-VI Compactor",
"18 Cu.m Heavy Duty Compactor"
],

"Mini Garbage Tipper":[
"2.5 Ton Hydraulic Tipper",
"3 Ton Municipal Tipper",
"2.8 Ton Diesel Tipper"
],

"Refuse Collector Vehicle":[
"12 Cu.m Refuse Collector",
"14 Cu.m Waste Collector",
"16 Cu.m Automatic Refuse Vehicle"
],

"Mechanical Road Sweeper":[
"5 Cu.m Mechanical Sweeper",
"6 Cu.m Dust Control Sweeper",
"High Efficiency Road Sweeper"
],

"Vacuum Road Sweeper":[
"6 Cu.m Vacuum Sweeper",
"7 Cu.m Heavy Vacuum Sweeper",
"High Suction Road Sweeper"
],

"Dumper Placer Vehicle":[
"6 Cu.m Dumper Placer",
"8 Cu.m Hydraulic Dumper",
"Heavy Duty Dumper Placer"
],

"Waste Collection Container":[
"1000 L HDPE Container",
"1100 L EN840 Container",
"UV Resistant Waste Bin"
],

"Hydraulic Waste Loader":[
"1.5 Cu.m Hydraulic Loader",
"2 Cu.m Loader",
"Heavy Duty Loader"
],

"Transfer Station Container":[
"5000 L Steel Container",
"5500 L Reinforced Container",
"Industrial Transfer Container"
],

"Plastic Baler Machine":[
"10 Ton Plastic Baler",
"12 Ton Hydraulic Baler",
"Semi Automatic Plastic Baler"
],

"Organic Waste Shredder":[
"500 Kg/hr Organic Shredder",
"750 Kg/hr Waste Shredder",
"Industrial Organic Shredder"
],

"Bio Waste Composting Machine":[
"500 Kg Compost Machine",
"750 Kg Compost Machine",
"Automatic Composting Unit"
],

"Portable Garbage Bin Set":[
"240 L HDPE Bin",
"240 L UV Resistant Bin",
"EN840 Bin Set"
],

"Skid Steer Loader":[
"60 HP Loader",
"70 HP Compact Loader",
"Premium Skid Loader"
],

"Waste Conveyor Belt Unit":[
"10 m Conveyor",
"12 m Conveyor",
"Industrial Sorting Conveyor"
],

"Industrial Waste Crusher":[
"20 HP Waste Crusher",
"25 HP Crusher",
"Heavy Duty Industrial Crusher"
],

"Dumpster Container":[
"1100 L Dumpster",
"1200 L Steel Dumpster",
"Reinforced Dumpster"
],

"Front Loader Waste Vehicle":[
"14 Cu.m Front Loader",
"16 Cu.m Waste Loader",
"Heavy Duty Front Loader"
],

"Waste Segregation Conveyor":[
"12 m Conveyor",
"15 m Conveyor",
"Industrial Conveyor Line"
]
}

# ======================================================
# ADDITIONAL SPECIFICATION LIBRARY
# ======================================================

SPECIFICATIONS.update({

# ---------------- WATER SUPPLY ----------------

"Water Tanker":[
"6000 L Stainless Steel Tanker",
"8000 L Municipal Water Tanker",
"10000 L Drinking Water Tanker"
],

"Chassis Mounted Water Tanker":[
"6000 L Chassis Mounted Tanker",
"8000 L BS-VI Water Tanker",
"Heavy Duty Water Supply Vehicle"
],

"Pipeline Leakage Detector":[
"Digital Ultrasonic Leakage Detector",
"Acoustic Pipeline Leak Detector",
"Smart Leak Detection Device"
],

"Portable Chlorination Unit":[
"1000 L/hr Chlorination System",
"Automatic Chlorination Unit",
"Municipal Water Chlorinator"
],

"Water Pumping Station Motor":[
"75 HP Pump Motor",
"100 HP Pump Motor",
"High Efficiency Pump Motor"
],

"Valve Testing Machine":[
"Hydraulic Valve Tester",
"Automatic Valve Testing Unit",
"Pressure Valve Calibration Machine"
],

"Pipe Pressure Monitoring Unit":[
"Digital Pressure Monitoring System",
"SCADA Pressure Sensor",
"IoT Pipeline Pressure Monitor"
],

"Water Quality Testing Kit":[
"Portable Water Testing Kit",
"Multi Parameter Water Analyzer",
"Digital Water Quality Lab Kit"
],

"Borewell Cleaning Machine":[
"Deep Borewell Cleaning Rig",
"Hydraulic Borewell Cleaner",
"Rotary Borewell Cleaning Machine"
],

"Pipeline Repair Vehicle":[
"Mobile Pipeline Repair Vehicle",
"Hydraulic Repair Van",
"Emergency Repair Vehicle"
],

"Pipeline Inspection Camera":[
"150 m HD Inspection Camera",
"Self Propelled Pipeline Camera",
"4K Sewer Inspection Camera"
],

"Water Purification Mobile Unit":[
"5000 L/day Mobile RO Plant",
"Portable Water Purification Van",
"Emergency Water Treatment Unit"
],

# ---------------- SEWERAGE ----------------

"Sewer Jetting Machine":[
"250 Bar High Pressure Jetter",
"300 Bar Sewer Jetting Machine",
"Truck Mounted Jetting Unit"
],

"Truck Mounted Suction Cum Jetting Machine":[
"5000 L Combined Jetting Vehicle",
"6000 L Vacuum Jetting Truck",
"BS-VI Suction Cum Jetting Machine"
],

"High Pressure Sewer Cleaner":[
"300 Bar Sewer Cleaner",
"Industrial Sewer Cleaner",
"Hydraulic Sewer Cleaning Unit"
],

"Sewer Inspection Camera":[
"150 m CCTV Inspection Camera",
"HD Sewer Inspection Robot",
"Digital Sewer Camera"
],

"Vacuum Sludge Tanker":[
"6000 L Vacuum Tanker",
"8000 L Sludge Extraction Tanker",
"Heavy Duty Vacuum Tanker"
],

"Sewer Cleaning Robot":[
"AI Enabled Sewer Robot",
"Remote Operated Sewer Robot",
"Crawler Inspection Robot"
],

# ---------------- DRAINAGE ----------------

"Drain Cleaning Machine":[
"Hydraulic Drain Cleaner",
"Portable Drain Cleaning Machine",
"Industrial Drain Cleaner"
],

"Portable Dewatering Pump":[
"30 HP Dewatering Pump",
"Diesel Dewatering Pump",
"Flood Control Pump"
],

"High Capacity Pump Set":[
"75 HP Flood Pump",
"100 HP Pump Set",
"Municipal Drainage Pump"
],

"Storm Water Pump":[
"Storm Water Pump 100 HP",
"Heavy Duty Flood Pump",
"Municipal Pump Set"
],

"Canal Desilting Machine":[
"Hydraulic Canal Desilter",
"Floating Desilting Machine",
"Heavy Duty Desilting Unit"
],

"Drain Jetting Machine":[
"250 Bar Drain Jetter",
"Drain Cleaning Jet Machine",
"High Pressure Drain Cleaner"
],

"Drain Inspection Camera":[
"HD Drain Inspection Camera",
"150 m Inspection Camera",
"Remote Drain Camera"
],

"Drain Clearing Robot":[
"Autonomous Drain Robot",
"AI Drain Cleaning Robot",
"Crawler Drain Robot"
],

# ---------------- ROAD ----------------

"Hydraulic Excavator":[
"20 Ton Hydraulic Excavator",
"22 Ton Excavator",
"Heavy Duty Excavator"
],

"Mini Excavator":[
"5 Ton Mini Excavator",
"6 Ton Compact Excavator",
"Hydraulic Mini Excavator"
],

"Backhoe Loader":[
"80 HP Backhoe Loader",
"90 HP Loader",
"Heavy Duty Backhoe"
],

"Road Roller":[
"10 Ton Vibratory Roller",
"12 Ton Road Roller",
"Hydraulic Compaction Roller"
],

"Vibratory Road Roller":[
"10 Ton Vibratory Roller",
"12 Ton Double Drum Roller",
"High Frequency Roller"
],

"Asphalt Paver Machine":[
"6 m Asphalt Paver",
"8 m Sensor Paver",
"Automatic Road Paver"
],

"Tipper Truck":[
"16 Ton Tipper",
"20 Ton Hydraulic Tipper",
"Heavy Duty Dump Truck"
],

"Dump Truck":[
"20 Ton Dump Truck",
"25 Ton Dump Truck",
"Mining Grade Dump Truck"
],

"Tyre Mounted Mobile Crane":[
"25 Ton Mobile Crane",
"40 Ton Hydraulic Crane",
"Heavy Lift Crane"
],

"Road Surface Milling Machine":[
"1 m Milling Machine",
"Cold Milling Machine",
"Road Rehabilitation Machine"
],

# ---------------- ELECTRICAL ----------------

"Diesel Generator Set":[
"125 KVA DG Set",
"250 KVA Generator",
"Silent Generator"
],

"Portable Generator":[
"25 KVA Generator",
"40 KVA Generator",
"Portable Diesel Generator"
],

"Street Light Maintenance Lift":[
"14 m Hydraulic Lift",
"16 m Maintenance Lift",
"Boom Lift Vehicle"
],

"Transformer Maintenance Vehicle":[
"Transformer Repair Vehicle",
"Power Utility Van",
"Electrical Maintenance Truck"
],

"Electric Cable Locator":[
"Digital Cable Locator",
"Underground Cable Detector",
"Cable Route Locator"
],

"Smart Street Light Controller":[
"IoT Smart Lighting Controller",
"Central Street Light Controller",
"Smart Pole Controller"
],

})

SPECIFICATIONS.update({

"Portable Waste Compactor":[
"10 Ton Portable Waste Compactor",
"12 Ton Hydraulic Compactor",
"Industrial Portable Compactor"
],

"Leaf Collection Vacuum Unit":[
"High Suction Leaf Collector",
"Industrial Leaf Vacuum",
"Municipal Leaf Collection Machine"
],

"Portable Bin Lifter":[
"240 L Hydraulic Bin Lifter",
"360 L Bin Handling Unit",
"Automatic Bin Lifting Machine"
],

"Waste Hopper Unit":[
"5 Cu.m Waste Hopper",
"8 Cu.m Steel Hopper",
"Heavy Duty Waste Hopper"
],

"Biomedical Waste Carrier":[
"Bio Waste Transport Vehicle",
"Medical Waste Carrier",
"Hazardous Waste Carrier"
],

"Municipal Waste Crane":[
"8 Ton Hydraulic Crane",
"Municipal Loading Crane",
"Truck Mounted Waste Crane"
],

"Street Cleaning Cart":[
"Manual Cleaning Cart",
"Heavy Duty Street Cart",
"Municipal Utility Cart"
],

"Waste Transfer Trailer":[
"15 Ton Waste Trailer",
"Heavy Duty Transfer Trailer",
"Municipal Transfer Trailer"
],

"Mobile Waste Collection Unit":[
"Compact Waste Collection Vehicle",
"Mini Waste Collection Van",
"Municipal Collection Unit"
],

"Root Cutting System for Sewer Line":[
"Hydraulic Root Cutter",
"Automatic Sewer Root Cutter",
"Heavy Duty Root Removal System"
],

"Portable Pipeline CCTV Unit":[
"Portable HD CCTV Inspection Unit",
"Pipeline Camera Kit",
"Digital Inspection System"
],

"Manhole Desilting Machine":[
"Hydraulic Desilting Machine",
"Vacuum Desilting Unit",
"Heavy Duty Manhole Cleaner"
],

"Portable Sludge Pump":[
"20 HP Sludge Pump",
"Diesel Sludge Pump",
"Portable Dewatering Pump"
],

"Drain Rodding Machine":[
"Mechanical Drain Rodder",
"Hydraulic Drain Rodder",
"Industrial Drain Cleaning Rodder"
],

"Underground Pipe Locator":[
"Digital Pipe Locator",
"Underground Utility Locator",
"Pipeline Detection System"
],

"Submersible Pump Unit":[
"15 HP Submersible Pump",
"30 HP Drainage Pump",
"Heavy Duty Pump Unit"
],

"Portable Flood Barrier Unit":[
"Inflatable Flood Barrier",
"Portable Flood Protection System",
"Rapid Flood Barrier"
],

"Emergency Drainage Vehicle":[
"Drainage Response Vehicle",
"Emergency Pump Vehicle",
"Flood Response Truck"
],

"Drain Excavation Unit":[
"Mini Excavation Unit",
"Hydraulic Drain Excavator",
"Municipal Excavation Machine"
],

"Portable Sandbag Filling Machine":[
"Automatic Sandbag Filler",
"Portable Sand Filling Unit",
"Emergency Sandbag Machine"
]

})



# ==========================================================
# EMERGENCY / SANITATION / SPECIALIZED SPECIFICATIONS
# ==========================================================

SPECIFICATIONS.update({

# ---------------- EMERGENCY ----------------

"Fire Tender Vehicle":[
"4500 L Water + 500 L Foam Tender",
"6000 L Fire Tender BS-VI",
"Quick Response Fire Tender"
],

"Portable Rescue Boat":[
"8 Person FRP Rescue Boat",
"Inflatable Flood Rescue Boat",
"Aluminium Rescue Boat"
],

"Emergency Ambulance Van":[
"ALS Ambulance BS-VI",
"BLS Ambulance",
"Advanced Life Support Ambulance"
],

"Emergency Water Pump":[
"30 HP Diesel Flood Pump",
"High Capacity Emergency Pump",
"Self Priming Flood Pump"
],

"Emergency Generator Unit":[
"125 KVA Emergency Generator",
"Silent DG Backup Unit",
"Automatic Backup Generator"
],

"Emergency Drone Surveillance Unit":[
"4K Thermal Drone",
"Long Range UAV",
"Disaster Surveillance Drone"
],

# ---------------- SANITATION ----------------

"Portable Toilet Unit":[
"FRP Portable Toilet",
"Premium Mobile Toilet",
"Bio Toilet Unit"
],

"Mobile Toilet Van":[
"6 Cabin Mobile Toilet",
"Luxury Mobile Toilet Van",
"Portable Washroom Vehicle"
],

"High Pressure Washer":[
"250 Bar Washer",
"Industrial Pressure Washer",
"Heavy Duty Cleaning Machine"
],

"Fogging Machine":[
"Thermal Fogging Machine",
"ULV Fogger",
"Vector Control Fogger"
],

"Street Disinfection Vehicle":[
"5000 L Disinfection Vehicle",
"Mounted Spray Vehicle",
"Municipal Sanitization Truck"
],

# ---------------- SPECIALIZED ----------------

"Air Quality Monitoring Station":[
"Continuous AQMS",
"Smart Air Quality Station",
"CPCB Approved AQMS"
],

"Municipal Survey Drone":[
"RTK Survey Drone",
"GIS Survey UAV",
"Photogrammetry Drone"
],

"GIS Mapping Workstation":[
"High Performance GIS Workstation",
"Planning Workstation",
"Urban GIS System"
],

"Smart Parking Monitoring Unit":[
"IoT Parking Sensor",
"Smart Parking Controller",
"ANPR Parking System"
],

"Smart Civic Monitoring Console":[
"Integrated Smart City Dashboard",
"Civic Monitoring Console",
"Urban Command Console"
],

"Integrated Utility Maintenance Vehicle":[
"Multi Utility Maintenance Vehicle",
"Integrated Municipal Utility Truck",
"Smart Utility Service Vehicle"
]

})
SPECIFICATIONS.update({

# ---------------- WATER SUPPLY ----------------

"Portable Mud Suction Unit":[
"3000 L Mud Suction Unit",
"Heavy Duty Sludge Suction Machine",
"Vacuum Mud Removal Unit"
],

"Portable Emergency Pump":[
"15 HP Emergency Pump",
"Portable Flood Pump",
"Diesel Emergency Pump"
],

"Flood Recovery Vehicle":[
"Flood Recovery Utility Vehicle",
"Water Removal Vehicle",
"Emergency Recovery Truck"
],

"Storm Drain Vacuum Cleaner":[
"High Vacuum Drain Cleaner",
"Storm Drain Cleaning Vehicle",
"Industrial Drain Vacuum Unit"
],

"Portable Water Diversion Unit":[
"Portable Water Diversion System",
"Emergency Flow Diversion Kit",
"Flood Diversion Barrier"
],

"Portable Water Storage Tank":[
"5000 L HDPE Water Tank",
"10000 L Emergency Storage Tank",
"Collapsible Water Storage Tank"
],

"Portable Pump Controller":[
"Digital Pump Controller",
"Automatic Pump Control Panel",
"Smart Pump Controller"
],

"Water Meter Calibration Unit":[
"Digital Water Meter Test Bench",
"Automatic Calibration Unit",
"Class 0.2 Calibration System"
],

"Reservoir Cleaning Machine":[
"Reservoir Cleaning Robot",
"Floating Reservoir Cleaner",
"Industrial Reservoir Cleaner"
],

"Portable Pipeline Flusher":[
"High Pressure Pipeline Flusher",
"Portable Pipe Cleaning Unit",
"Hydraulic Pipeline Flushing System"
],

"Hydraulic Pipe Cutter":[
"Hydraulic Pipe Cutting Machine",
"Industrial Pipe Cutter",
"Portable Hydraulic Cutter"
],

"Portable Water Pump Unit":[
"10 HP Portable Water Pump",
"Diesel Water Pump",
"Portable Centrifugal Pump"
],

"Emergency Water Supply Vehicle":[
"Emergency Water Tanker",
"Mobile Water Supply Vehicle",
"Disaster Water Supply Truck"
],

"Smart Water Monitoring Sensor":[
"IoT Water Monitoring Sensor",
"Digital Water Pressure Sensor",
"Smart Water Quality Sensor"
],

"Water Pipeline Maintenance Kit":[
"Complete Pipeline Repair Kit",
"Municipal Maintenance Toolkit",
"Emergency Pipeline Service Kit"
],

# ---------------- ROAD INFRA ----------------

"Wheel Loader":[
"2 Cu.m Wheel Loader",
"3 Cu.m Hydraulic Loader",
"Heavy Duty Wheel Loader"
],

"Track Mounted Excavator":[
"22 Ton Track Excavator",
"Crawler Excavator",
"Heavy Duty Hydraulic Excavator"
],

"Concrete Mixer Machine":[
"500 L Concrete Mixer",
"750 L Mixer Machine",
"Heavy Duty Concrete Mixer"
],

"Concrete Vibrator":[
"Electric Concrete Vibrator",
"High Frequency Vibrator",
"Industrial Concrete Vibrator"
]


})
SPECIFICATIONS.update({

# ---------------- ROAD INFRA ----------------

"Asphalt Cutter":[
"14 HP Asphalt Cutter",
"Hydraulic Asphalt Cutting Machine",
"Heavy Duty Road Cutter"
],

"Road Marking Machine":[
"Thermoplastic Road Marking Machine",
"Self Propelled Marking Machine",
"Automatic Lane Marking Unit"
],

"Concrete Cutting Machine":[
"16 HP Concrete Cutter",
"Diamond Blade Concrete Cutter",
"Heavy Duty Concrete Cutting Machine"
],

"Crack Sealing Machine":[
"Hot Melt Crack Sealer",
"Road Crack Filling Machine",
"Automatic Crack Sealing Unit"
],

"Portable Concrete Pump":[
"30 m Concrete Pump",
"Trailer Mounted Concrete Pump",
"Portable Hydraulic Concrete Pump"
],

"Hydraulic Breaker":[
"20 Ton Hydraulic Breaker",
"Rock Breaker Attachment",
"Heavy Duty Hydraulic Hammer"
],

"Portable Generator for Road Work":[
"25 KVA Road Generator",
"Silent Portable Generator",
"Construction Site Generator"
],

"Traffic Cone Deployment Unit":[
"Automatic Traffic Cone Deployer",
"Road Safety Cone Machine",
"Highway Cone Deployment System"
],

"Road Repair Patch Machine":[
"Automatic Road Patching Machine",
"Asphalt Patch Repair Unit",
"Road Maintenance Machine"
],

"Curb Stone Laying Machine":[
"Automatic Kerb Paver",
"Hydraulic Curb Stone Laying Machine",
"Road Kerb Installation Machine"
],

"Pavement Compactor":[
"Hydraulic Pavement Compactor",
"Walk Behind Compactor",
"Heavy Duty Plate Compactor"
],

# ---------------- ELECTRICAL ----------------

"Underground Fault Detector":[
"Digital Cable Fault Locator",
"Underground Fault Detection System",
"HV Cable Fault Detector"
],

"Portable Tower Light":[
"9 m LED Tower Light",
"Diesel Tower Light",
"Mobile Lighting Tower"
],

"Electrical Maintenance Van":[
"Electrical Service Van",
"Power Utility Maintenance Vehicle",
"Electrical Repair Vehicle"
],

"Portable Solar Lighting Unit":[
"Portable Solar Tower Light",
"Solar LED Lighting Unit",
"Emergency Solar Lighting System"
],

"Mobile Repair Van":[
"Municipal Repair Van",
"Utility Service Vehicle",
"Integrated Maintenance Van"
],

"Voltage Monitoring Device":[
"Digital Voltage Monitor",
"3 Phase Voltage Analyzer",
"Smart Voltage Monitoring Unit"
],

"Underground Cable Repair Kit":[
"11 kV Cable Repair Kit",
"XLPE Cable Jointing Kit",
"Underground Cable Maintenance Kit"
],

"Portable Battery Backup Unit":[
"Portable Lithium Battery Backup",
"UPS Battery Backup Unit",
"Emergency Battery Power Pack"
],

"Smart Utility Monitoring Console":[
"Integrated Utility Dashboard",
"SCADA Monitoring Console",
"Smart Utility Command Console"
]

})
SPECIFICATIONS.update({

# -------- SANITATION --------

"Public Toilet Cleaning Machine":[
"High Pressure Toilet Cleaning Machine",
"Automatic Washroom Cleaning System",
"Municipal Toilet Maintenance Machine"
],

"Disinfection Sprayer Unit":[
"500 L Disinfection Sprayer",
"Vehicle Mounted Sanitization Sprayer",
"High Pressure Spray Unit"
],

"Portable Cleaning Cart":[
"Municipal Cleaning Cart",
"Heavy Duty Utility Cart",
"Maintenance Service Cart"
],

"Manual Cleaning Trolley":[
"Janitorial Cleaning Trolley",
"Municipal Cleaning Trolley",
"Multi Utility Cleaning Cart"
],

"Portable Hand Wash Station":[
"Mobile Hand Wash Station",
"Foot Operated Wash Station",
"Portable Hygiene Unit"
],

"Sanitary Waste Disposal Unit":[
"Bio Waste Disposal Unit",
"Sanitary Waste Collection Unit",
"Medical Waste Bin"
],

"Portable Urinal Unit":[
"Portable Public Urinal",
"Mobile Urinal Cabin",
"FRP Urinal Unit"
],

"Public Washroom Maintenance Vehicle":[
"Washroom Service Vehicle",
"Municipal Cleaning Van",
"Utility Maintenance Vehicle"
],

"Drain Disinfection Unit":[
"Drain Sanitization Machine",
"Chemical Spray Unit",
"Drain Disinfection System"
],

"Portable Steam Cleaning Machine":[
"Industrial Steam Cleaner",
"Portable Steam Washer",
"High Temperature Cleaner"
],

"Biohazard Disposal Container":[
"Medical Waste Container",
"Biohazard Bin",
"Infectious Waste Container"
],

"Portable Sanitation Kiosk":[
"Portable Hygiene Booth",
"Public Sanitation Kiosk",
"Smart Hygiene Unit"
],

"Municipal Cleaning Utility Vehicle":[
"Utility Cleaning Vehicle",
"Compact Cleaning Vehicle",
"Municipal Service Vehicle"
],

# -------- EMERGENCY --------

"Emergency Communication Van":[
"Emergency Command Van",
"Communication Response Vehicle",
"Mobile Incident Control Van"
],

"Portable Medical Response Unit":[
"Emergency Medical Kit",
"Portable Response Unit",
"Mobile Medical Support Unit"
],

"Debris Removal Loader":[
"Debris Loader",
"Municipal Debris Loader",
"Hydraulic Debris Loader"
],

"Portable Lighting Tower":[
"LED Lighting Tower",
"Diesel Lighting Tower",
"Emergency Lighting Mast"
],

"Portable Emergency Shelter Unit":[
"Emergency Shelter Tent",
"Rapid Shelter Unit",
"Portable Relief Shelter"
],

"Hydraulic Rescue Cutter":[
"Hydraulic Rescue Tool",
"Emergency Cutter Spreader",
"Vehicle Rescue Cutter"
],

"Emergency Evacuation Vehicle":[
"Emergency Transport Vehicle",
"Disaster Evacuation Vehicle",
"Rapid Response Vehicle"
],

"Portable Public Warning System":[
"Portable PA System",
"Emergency Warning Unit",
"Mobile Alert System"
],

"Flood Monitoring Sensor":[
"IoT Flood Sensor",
"River Level Monitoring Sensor",
"Smart Flood Detection Unit"
],

"Portable Life Support Kit":[
"Emergency Life Support Kit",
"Advanced First Aid Kit",
"Portable Medical Support Kit"
],

"Disaster Recovery Crane":[
"Recovery Crane",
"Emergency Lifting Crane",
"Heavy Duty Rescue Crane"
],

"Portable Command Center Unit":[
"Mobile Command Center",
"Emergency Control Unit",
"Incident Command Vehicle"
],

"Rapid Response Vehicle":[
"Rapid Response SUV",
"Emergency Utility Vehicle",
"Disaster Response Vehicle"
],

"Emergency Traffic Diversion Unit":[
"Traffic Diversion Trailer",
"Emergency Traffic Control Kit",
"Road Diversion Unit"
],

"Portable Search Light Unit":[
"LED Search Light",
"Portable Rescue Light",
"Emergency Search Lamp"
],

"Disaster Supply Transport Vehicle":[
"Relief Supply Truck",
"Emergency Cargo Vehicle",
"Disaster Logistics Vehicle"
],

# -------- ENVIRONMENT --------

"Sewage Treatment Plant Pump":[
"75 HP STP Pump",
"100 HP Sewage Pump",
"Industrial STP Pump"
],

"Portable Laboratory Testing Unit":[
"Mobile Laboratory",
"Water Testing Lab Van",
"Portable Testing Station"
],

"Noise Pollution Monitoring Unit":[
"Noise Monitoring Station",
"Portable Noise Meter",
"Environmental Noise Monitor"
],

"Construction Debris Crusher":[
"Construction Waste Crusher",
"Mobile Debris Crusher",
"Concrete Rubble Crusher"
],

"Portable Air Compressor":[
"Diesel Air Compressor",
"Portable Compressor",
"Industrial Air Compressor"
],

"Industrial Pollution Response Unit":[
"Pollution Response Vehicle",
"Hazardous Material Response Unit",
"Environmental Emergency Vehicle"
],

"Portable Municipal Command Vehicle":[
"Municipal Command Vehicle",
"Mobile Civic Command Center",
"Integrated Municipal Operations Van"
]
})


# ==========================================================
# GENERATE VENDORS
# ==========================================================

for _, equip in equipment_df.iterrows():

    equipment_name = str(equip["equipment_name"]).strip()

    equipment_type = equip["operational_type"]

    vendors = VENDOR_MAP.get(
        equipment_type,
        ["L&T", "BEML", "Tata Motors"]
    )

    equipment_name = str(equipment_name).strip()

    if equipment_name not in SPECIFICATIONS:
        raise ValueError(
            f"Specification missing for equipment: {equipment_name}"
    )

    specs = SPECIFICATIONS[equipment_name]

    selected_vendors = random.sample(
        vendors,
        min(3, len(vendors))
    )

    for vendor in selected_vendors:

        base_price = float(equip["unit_cost_lakhs"])

        price = round(
            random.uniform(
                base_price * 0.95,
                base_price * 1.08
            ),
            2
        )

        quality = random.randint(90,98)

        rating = round(
            random.uniform(4.4,4.9),
            1
        )

        delivery = random.randint(10,30)

        warranty = random.randint(3,5)

        gem = random.choice(["Yes","Yes","Yes","No"])

        specification = random.choice(specs)

        vendor_records.append({

            "vendor_id":
                f"V{vendor_counter:03d}",

            "vendor_name":
                vendor,

            "equipment_id":
                equip["equipment_id"],

            "equipment_name":
                equipment_name,

            "specification":
                specification,

            "quoted_price_lakhs":
                price,

            "quality_score":
                quality,

            "delivery_days":
                delivery,

            "warranty_years":
                warranty,

            "vendor_rating":
                rating,

            "gem_available":
                gem

        })

        vendor_counter += 1

# ==========================================================
# SAVE CSV
# ==========================================================

vendor_df = pd.DataFrame(vendor_records)

vendor_df.to_csv(
    "data/raw/vendor_database.csv",
    index=False
)

print("="*60)
print("Vendor Database Generated Successfully")
print("="*60)
print(f"Total Vendors : {len(vendor_df)}")
print("Saved to : data/raw/vendor_database.csv")
print("="*60)