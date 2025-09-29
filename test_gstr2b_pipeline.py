#!/usr/bin/env python3
"""
Test script to verify GSTR2B pipeline works correctly with the provided JSON file.
"""

import json
import sys
from gstr2b_dedicated_processor import GSTR2BDedicatedProcessor
from gstr2b_masters_xml import GSTR2BMastersXMLGenerator
from gstr2b_transactions_xml import GSTR2BTransactionsXMLGenerator

def test_gstr2b_pipeline():
    """Test the complete GSTR2B processing pipeline."""
    
    # Load the sample GSTR2B JSON file
    try:
        with open('attached_assets/gstr2b_sample_1759141356638.json', 'r') as f:
            gstr2b_data = json.load(f)
        print("✅ Successfully loaded GSTR2B JSON file")
    except Exception as e:
        print(f"❌ Failed to load GSTR2B JSON file: {e}")
        return False
    
    # Initialize processor
    company_state = "Delhi"
    processor = GSTR2BDedicatedProcessor(company_state)
    
    # Validate data
    print("\n🔍 Validating GSTR2B data structure...")
    validation_result = processor.validate_gstr2b_data(gstr2b_data)
    
    if validation_result['valid']:
        print("✅ GSTR2B data structure is valid")
        for warning in validation_result['warnings']:
            print(f"⚠️  {warning}")
    else:
        print("❌ GSTR2B data validation failed:")
        for error in validation_result['errors']:
            print(f"   • {error}")
        return False
    
    # Process GSTR2B data
    print("\n🔄 Processing GSTR2B data...")
    try:
        vendors, invoices, metadata = processor.process_gstr2b_json(gstr2b_data)
        print(f"✅ Successfully processed {len(vendors)} vendors with {len(invoices)} invoices")
        
        # Print summary
        summary = processor.get_vendor_summary(vendors)
        print(f"\n📊 Summary:")
        print(f"   • Total Vendors: {summary.get('total_vendors', 0)}")
        print(f"   • Total Invoices: {summary.get('total_invoices', 0)}")
        print(f"   • Total Taxable Value: ₹{summary.get('total_taxable_value', 0):,.2f}")
        print(f"   • Total Tax Amount: ₹{summary.get('total_tax_amount', 0):,.2f}")
        
    except Exception as e:
        print(f"❌ Error processing GSTR2B data: {e}")
        return False
    
    # Test Masters XML Generation
    print("\n🏛️ Testing Masters XML generation...")
    company_name = "Test Company Ltd"
    try:
        masters_generator = GSTR2BMastersXMLGenerator(company_name, company_state)
        masters_validation = masters_generator.validate_masters_xml(vendors)
        
        if masters_validation['valid']:
            print("✅ Masters XML validation passed")
            masters_xml = masters_generator.generate_masters_xml(vendors, metadata)
            if masters_xml and len(masters_xml) > 100:
                print(f"✅ Masters XML generated successfully ({len(masters_xml):,} characters)")
            else:
                print("❌ Masters XML generation failed or empty")
                return False
        else:
            print("❌ Masters XML validation failed:")
            for error in masters_validation['errors']:
                print(f"   • {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating Masters XML: {e}")
        return False
    
    # Test Transactions XML Generation
    print("\n📄 Testing Transactions XML generation...")
    try:
        transactions_generator = GSTR2BTransactionsXMLGenerator(company_name, company_state)
        transactions_validation = transactions_generator.validate_transactions_xml(invoices)
        
        if transactions_validation['valid']:
            print("✅ Transactions XML validation passed")
            summary = transactions_validation['summary']
            print(f"   • Total Invoices: {summary['total_invoices']}")
            print(f"   • Interstate: {summary['interstate_invoices']}, Intrastate: {summary['intrastate_invoices']}")
            
            transactions_xml = transactions_generator.generate_transactions_xml(invoices, metadata)
            if transactions_xml and len(transactions_xml) > 100:
                print(f"✅ Transactions XML generated successfully ({len(transactions_xml):,} characters)")
            else:
                print("❌ Transactions XML generation failed or empty")
                return False
        else:
            print("❌ Transactions XML validation failed:")
            for error in transactions_validation['errors']:
                print(f"   • {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating Transactions XML: {e}")
        return False
    
    print("\n🎉 All tests passed! GSTR2B pipeline is working correctly.")
    return True

if __name__ == "__main__":
    success = test_gstr2b_pipeline()
    sys.exit(0 if success else 1)