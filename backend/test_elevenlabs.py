import asyncio
import os
from dotenv import load_dotenv
from app.services.voice_service import voice_service

# Load environment variables
load_dotenv()


async def test_voice_generation():
    print("Testing ElevenLabs Voice Generation...")

    # Using the Narrator text from your placeholder script
    test_script = (
        '''
        Five hundred thousand square miles of open ocean. Over one thousand lives lost. And not a single trace left behind. Welcome to the Bermuda Triangle, the world’s most infamous graveyard.
        It first captured the world's imagination in 1945 when Flight 19—a squadron of five US Navy bombers—vanished during a routine training mission. When the rescue plane sent to find them also disappeared, the legend was born.

        The theories are as wild as the waves. Some believe the lost city of Atlantis sits at the bottom, using ancient crystal energy to pull ships down. Others claim it's a portal for extraterrestrial abductions or a rip in the space-time continuum where compasses spin out of control.

        But what does science say? Geologists point to massive deposits of methane gas trapped under the seafloor. If these pockets burst, they could theoretically lower water density enough to sink a ship instantly. Then there are rogue waves—walls of water reaching one hundred feet high—and the Gulf Stream, a powerful current that can carry debris hundreds of miles away in minutes.
        
        Here is the most shocking part: Statistically, the Bermuda Triangle isn't actually that dangerous. According to the World Wildlife Fund and major insurance companies, there are no more disappearances here than in any other heavily traveled part of the ocean. It’s one of the busiest shipping lanes in the world, and most vessels pass through without a scratch.
        
        Is the mystery solved, or is there something the data isn't telling us? Whether it’s magnetic anomalies or just bad luck, the Bermuda Triangle continues to haunt our curiosity. What do you think is happening down there? Let us know in the comments. Don’t forget to like and subscribe for more mysteries. See you in the next one.
        '''
    )

    print("Generating voiceover...")
    output_path = await voice_service.generate_voiceover(test_script, "bermuda_placeholder_test.mp3")

    print("\nResults:")
    if not output_path.startswith("Error"):
        print(f"Success! Audio saved to: {output_path}")
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"File size: {file_size} bytes")
        else:
            print("Error: File was not actually created on disk.")
    else:
        print(f"Generation failed: {output_path}")

if __name__ == "__main__":
    asyncio.run(test_voice_generation())
