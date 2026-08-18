# =================================================================
# FILE: worker/run_comprehensive_tests.py
# Comprehensive testing suite to validate all presets and processing quality
# =================================================================
import asyncio
import os
import sys
import json
import shutil
from datetime import datetime
from types import SimpleNamespace
from pathlib import Path

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.jobs.enhance_from_audio import enhance_from_audio
from app.jobs.enhance_from_text import enhance_from_text
from app.presets import PRO_COOKBOOK_DEFINITIVE_FINAL, PRO_COOKBOOK_V1

class MockSupabaseClient:
    """Mock Supabase client for testing."""
    def __init__(self, test_data):
        self._test_data = test_data
    
    def table(self, table_name):
        return self
    
    def update(self, data):
        print(f"[MOCK DB UPDATE] {data}")
        return self
    
    def select(self, *args, **kwargs):
        return self
    
    def eq(self, column, value):
        return self
    
    def single(self):
        return self
    
    def execute(self):
        return SimpleNamespace(data=self._test_data)

class ComprehensiveTestSuite:
    """Comprehensive testing suite for all audio processing."""
    
    def __init__(self):
        self.test_results = []
        self.output_dir = "test_outputs"
        self.test_audio_dir = "test_audio_samples"
        
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/audio_to_audio", exist_ok=True)
        os.makedirs(f"{self.output_dir}/text_to_audio", exist_ok=True)
        os.makedirs(f"{self.output_dir}/reports", exist_ok=True)
        
        print("=" * 80)
        print("VOXORA COMPREHENSIVE TEST SUITE v3.0")
        print("=" * 80)
        print(f"Output Directory: {self.output_dir}")
        print(f"Test Audio Directory: {self.test_audio_dir}")
        print()
    
    async def test_audio_to_audio_preset(self, input_file: str, preset_name: str):
        """Test a single Audio-to-Audio preset."""
        
        test_id = f"a2a_{preset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\nTesting Audio-to-Audio: {preset_name}")
        print(f"Input File: {input_file}")
        print(f"Test ID: {test_id}")
        print("-" * 60)
        
        # Setup mock context
        mock_data = {'preset': preset_name}
        ctx = {'supabase': MockSupabaseClient(mock_data)}
        
        # Run the enhancement
        try:
            start_time = datetime.now()
            success = await enhance_from_audio(ctx, test_id, input_file)
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            
            # Check if output file exists
            output_file = f"{test_id}.mp3"
            output_exists = os.path.exists(output_file)
            
            if output_exists:
                file_size = os.path.getsize(output_file)
                
                # Move to organized output directory
                output_path = f"{self.output_dir}/audio_to_audio/{preset_name}_{test_id}.mp3"
                shutil.move(output_file, output_path)
                
                result = {
                    'test_type': 'audio_to_audio',
                    'preset': preset_name,
                    'input_file': input_file,
                    'test_id': test_id,
                    'success': success,
                    'processing_time_seconds': processing_time,
                    'output_file': output_path,
                    'output_size_bytes': file_size,
                    'output_size_mb': round(file_size / (1024 * 1024), 2),
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"SUCCESS: Output saved to {output_path}")
                print(f"Processing Time: {processing_time:.2f} seconds")
                print(f"Output Size: {result['output_size_mb']} MB")
            else:
                result = {
                    'test_type': 'audio_to_audio',
                    'preset': preset_name,
                    'input_file': input_file,
                    'test_id': test_id,
                    'success': False,
                    'processing_time_seconds': processing_time,
                    'error': 'Output file not created',
                    'timestamp': datetime.now().isoformat()
                }
                print(f"FAILED: No output file created")
        
        except Exception as e:
            result = {
                'test_type': 'audio_to_audio',
                'preset': preset_name,
                'input_file': input_file,
                'test_id': test_id,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"ERROR: {str(e)}")
        
        self.test_results.append(result)
        return result
    
    async def test_text_to_audio_preset(self, text: str, preset_name: str, voice_name: str = None):
        """Test a single Text-to-Audio preset."""
        
        test_id = f"t2a_{preset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\nTesting Text-to-Audio: {preset_name}")
        print(f"Text Length: {len(text)} characters")
        print(f"Voice: {voice_name or 'Default from preset'}")
        print(f"Test ID: {test_id}")
        print("-" * 60)
        
        # Setup mock context
        mock_data = {
            'input_text': text,
            'preset': preset_name,
            'selected_voice': voice_name
        }
        ctx = {'supabase': MockSupabaseClient(mock_data)}
        
        # Run the enhancement
        try:
            start_time = datetime.now()
            success = await enhance_from_text(ctx, test_id)
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            
            # Check if output file exists
            output_file = f"{test_id}.mp3"
            output_exists = os.path.exists(output_file)
            
            if output_exists:
                file_size = os.path.getsize(output_file)
                
                # Move to organized output directory
                output_path = f"{self.output_dir}/text_to_audio/{preset_name}_{test_id}.mp3"
                shutil.move(output_file, output_path)
                
                result = {
                    'test_type': 'text_to_audio',
                    'preset': preset_name,
                    'voice': voice_name,
                    'text_length': len(text),
                    'test_id': test_id,
                    'success': success,
                    'processing_time_seconds': processing_time,
                    'output_file': output_path,
                    'output_size_bytes': file_size,
                    'output_size_mb': round(file_size / (1024 * 1024), 2),
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"SUCCESS: Output saved to {output_path}")
                print(f"Processing Time: {processing_time:.2f} seconds")
                print(f"Output Size: {result['output_size_mb']} MB")
            else:
                result = {
                    'test_type': 'text_to_audio',
                    'preset': preset_name,
                    'voice': voice_name,
                    'test_id': test_id,
                    'success': False,
                    'processing_time_seconds': processing_time,
                    'error': 'Output file not created',
                    'timestamp': datetime.now().isoformat()
                }
                print(f"FAILED: No output file created")
        
        except Exception as e:
            result = {
                'test_type': 'text_to_audio',
                'preset': preset_name,
                'voice': voice_name,
                'test_id': test_id,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"ERROR: {str(e)}")
        
        self.test_results.append(result)
        return result
    
    async def run_all_audio_to_audio_tests(self):
        """Test all Audio-to-Audio presets with available input files."""
        
        print("\n" + "=" * 80)
        print("AUDIO-TO-AUDIO COMPREHENSIVE TESTING")
        print("=" * 80)
        
        # Find all test audio files
        test_files = []
        if os.path.exists(self.test_audio_dir):
            for file in os.listdir(self.test_audio_dir):
                if file.endswith(('.mp3', '.wav', '.m4a', '.ogg', '.flac')):
                    test_files.append(os.path.join(self.test_audio_dir, file))
        
        if not test_files:
            print(f"\nWARNING: No test audio files found in {self.test_audio_dir}")
            print("Please add test audio files to continue.")
            print("Supported formats: .mp3, .wav, .m4a, .ogg, .flac")
            return
        
        print(f"\nFound {len(test_files)} test audio file(s)")
        
        # Test each preset with each file
        all_presets = list(PRO_COOKBOOK_DEFINITIVE_FINAL.keys())
        total_tests = len(all_presets) * len(test_files)
        
        print(f"Testing {len(all_presets)} presets with {len(test_files)} file(s)")
        print(f"Total tests: {total_tests}")
        
        test_count = 0
        for input_file in test_files:
            for preset_name in all_presets:
                test_count += 1
                print(f"\n[Test {test_count}/{total_tests}]")
                await self.test_audio_to_audio_preset(input_file, preset_name)
    
    async def run_all_text_to_audio_tests(self):
        """Test all Text-to-Audio presets with sample texts."""
        
        print("\n" + "=" * 80)
        print("TEXT-TO-AUDIO COMPREHENSIVE TESTING")
        print("=" * 80)
        
        # Sample texts for different use cases
        test_texts = {
            'podcast_intro': "Welcome to the Voxora podcast, where we explore the cutting edge of audio technology. Today, we're discussing the future of voice synthesis and how AI is revolutionizing content creation.",
            
            'audiobook_sample': "Chapter One. The morning sun cast long shadows across the valley as Sarah began her journey. She had prepared for this moment for years, yet nothing could have truly prepared her for what lay ahead. The path wound through ancient forests, where secrets older than memory itself waited to be discovered.",
            
            'educational_content': "In this lesson, we'll explore the fundamental principles of audio processing. First, let's understand what frequency means. Frequency refers to the number of sound wave cycles per second, measured in Hertz. Lower frequencies create bass sounds, while higher frequencies create treble sounds.",
            
            'commercial_script': "Introducing the all-new Voxora Pro. Transform your audio with professional-grade enhancement. Crystal clear sound. Broadcast quality. Studio results. Try it free today.",
            
            'short_announcement': "Attention all users. The system will be undergoing maintenance tonight from midnight to 2 AM. Thank you for your patience."
        }
        
        all_presets = list(PRO_COOKBOOK_V1.keys())
        total_tests = len(all_presets) * len(test_texts)
        
        print(f"\nTesting {len(all_presets)} presets with {len(test_texts)} text samples")
        print(f"Total tests: {total_tests}")
        
        test_count = 0
        for text_name, text_content in test_texts.items():
            for preset_name in all_presets:
                test_count += 1
                print(f"\n[Test {test_count}/{total_tests}] - {text_name}")
                await self.test_text_to_audio_preset(text_content, preset_name)
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        
        print("\n" + "=" * 80)
        print("GENERATING TEST REPORT")
        print("=" * 80)
        
        # Calculate statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.get('success'))
        failed_tests = total_tests - successful_tests
        
        a2a_tests = [r for r in self.test_results if r['test_type'] == 'audio_to_audio']
        t2a_tests = [r for r in self.test_results if r['test_type'] == 'text_to_audio']
        
        a2a_success = sum(1 for r in a2a_tests if r.get('success'))
        t2a_success = sum(1 for r in t2a_tests if r.get('success'))
        
        # Calculate average processing times
        successful_results = [r for r in self.test_results if r.get('success')]
        if successful_results:
            avg_processing_time = sum(r['processing_time_seconds'] for r in successful_results) / len(successful_results)
            total_output_size = sum(r.get('output_size_mb', 0) for r in successful_results)
        else:
            avg_processing_time = 0
            total_output_size = 0
        
        # Generate report
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'success_rate': f"{(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"
            },
            'audio_to_audio': {
                'total_tests': len(a2a_tests),
                'successful': a2a_success,
                'failed': len(a2a_tests) - a2a_success,
                'success_rate': f"{(a2a_success/len(a2a_tests)*100):.1f}%" if a2a_tests else "0%"
            },
            'text_to_audio': {
                'total_tests': len(t2a_tests),
                'successful': t2a_success,
                'failed': len(t2a_tests) - t2a_success,
                'success_rate': f"{(t2a_success/len(t2a_tests)*100):.1f}%" if t2a_tests else "0%"
            },
            'performance': {
                'average_processing_time_seconds': round(avg_processing_time, 2),
                'total_output_size_mb': round(total_output_size, 2)
            },
            'detailed_results': self.test_results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save JSON report
        report_file = f"{self.output_dir}/reports/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\nTEST SUMMARY:")
        print(f"  Total Tests: {total_tests}")
        print(f"  Successful: {successful_tests} ({report['test_summary']['success_rate']})")
        print(f"  Failed: {failed_tests}")
        print(f"\nAUDIO-TO-AUDIO:")
        print(f"  Tests: {len(a2a_tests)}")
        print(f"  Success Rate: {report['audio_to_audio']['success_rate']}")
        print(f"\nTEXT-TO-AUDIO:")
        print(f"  Tests: {len(t2a_tests)}")
        print(f"  Success Rate: {report['text_to_audio']['success_rate']}")
        print(f"\nPERFORMANCE:")
        print(f"  Avg Processing Time: {avg_processing_time:.2f}s")
        print(f"  Total Output Size: {total_output_size:.2f} MB")
        print(f"\nDetailed report saved to: {report_file}")
        
        # Print failed tests details
        if failed_tests > 0:
            print(f"\nFAILED TESTS DETAILS:")
            for result in self.test_results:
                if not result.get('success'):
                    print(f"\n  Preset: {result['preset']}")
                    print(f"  Type: {result['test_type']}")
                    print(f"  Error: {result.get('error', 'Unknown')}")
        
        return report

async def main():
    """Main test runner."""
    
    suite = ComprehensiveTestSuite()
    
    print("\nVOXORA COMPREHENSIVE TEST SUITE")
    print("This will test all presets with all available audio samples")
    print()
    print("Test Types:")
    print("  1. Audio-to-Audio Enhancement (all presets)")
    print("  2. Text-to-Audio Generation (all presets)")
    print("  3. Both")
    print()
    
    choice = input("Select test type (1/2/3) [3]: ").strip() or "3"
    
    if choice in ['1', '3']:
        await suite.run_all_audio_to_audio_tests()
    
    if choice in ['2', '3']:
        await suite.run_all_text_to_audio_tests()
    
    # Generate final report
    suite.generate_test_report()
    
    print("\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)
    print(f"\nAll outputs saved to: {suite.output_dir}")
    print("\nNext Steps:")
    print("  1. Listen to all output files in test_outputs/")
    print("  2. Compare quality against free tools (Adobe Audition, Descript)")
    print("  3. Identify which presets need improvement")
    print("  4. Document specific quality issues")
    print("  5. Only proceed with frontend if results justify premium pricing")

if __name__ == "__main__":
    asyncio.run(main())