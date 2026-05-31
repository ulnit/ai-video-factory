#!/usr/bin/env python3
"""
AI Video Factory — Fully automated video content generator.
Script → Slides → Captions → MP4. No camera, no mic, no human needed.
"""
import subprocess
import os
import json
import time
import random
import textwrap
from datetime import datetime
from pathlib import Path

# Optional: Pillow for slide generation
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

WORK_DIR = Path(__file__).parent.parent
OUTPUT_DIR = WORK_DIR / "output"

# Video topics database
TOPICS = {
    "ai_tools": [
        "5 AI Tools That Will Save You 10 Hours Per Week",
        "Best Free AI Tools in 2026 — Complete Guide",
        "How to Make Money With AI Tools (No Experience)",
        "AI vs Human: Who Writes Better Code?",
        "The Only AI Tools You Need in 2026",
    ],
    "tech_trends": [
        "Top 5 Tech Trends That Will Dominate 2026",
        "Why Everyone Is Switching to AI Agents",
        "The End of Traditional Software Development",
        "How AI Is Changing Every Industry in 2026",
        "What OpenAI, Google, and Microsoft Are Hiding",
    ],
    "make_money": [
        "5 Passive Income Streams Using AI in 2026",
        "How I Make $5,000/Month With AI Automation",
        "Side Hustles That AI Can Run For You 24/7",
        "From $0 to $1,000: AI Side Hustle Blueprint",
        "The Lazy Person's Guide to AI Income",
    ],
    "tutorials": [
        "How to Build an AI Agent in 10 Minutes",
        "Python Automation Tutorial for Beginners",
        "Setup a Raspberry Pi AI Server (Full Guide)",
        "Create a ChatGPT Clone With Python",
        "Automate Your Entire Workflow With AI",
    ],
}

def generate_script(topic=None, num_slides=8):
    """Generate a video script with slide-by-slide content"""
    category = "general"
    if topic is None:
        category = random.choice(list(TOPICS.keys()))
        topic = random.choice(TOPICS[category])
    else:
        # Find category for provided topic
        for cat, topics in TOPICS.items():
            if topic in topics:
                category = cat
                break
    
    script = {
        "title": topic,
        "category": category if topic in TOPICS.get(category, []) else "general",
        "slides": [],
        "captions": [],
    }
    
    # Intro slide
    script["slides"].append({
        "type": "title",
        "text": topic,
        "subtitle": "AI Video Factory — Automated Content",
        "duration": 4,
    })
    
    # Content slides
    contents = generate_content(topic, num_slides - 2)
    for i, content in enumerate(contents):
        script["slides"].append({
            "type": "content",
            "title": content["heading"],
            "text": content["body"],
            "bullet": i + 1,
            "duration": content.get("duration", 6),
        })
        script["captions"].extend(content.get("captions", []))
    
    # Outro slide
    script["slides"].append({
        "type": "outro",
        "text": "Subscribe for more AI automation!",
        "subtitle": "Built by AI on a $35 Raspberry Pi",
        "duration": 4,
    })
    
    return script

def generate_content(topic, count):
    """Generate slide content based on topic"""
    templates = [
        {"heading": "The Problem", "body": "Most people waste hours on repetitive tasks every single day. But there's a better way.", "captions": ["Most people waste hours on repetitive tasks.", "But there's a better way."]},
        {"heading": "The Solution", "body": "AI tools can automate 80% of your daily workflow. Here are the top picks for 2026.", "captions": ["AI tools can automate 80% of your daily workflow.", "Here are the top picks for 2026."]},
        {"heading": "Tool #1: ChatGPT", "body": "The most powerful AI assistant. Use it for writing, coding, research, and more.", "captions": ["ChatGPT: The most powerful AI assistant.", "Use it for writing, coding, research, and more."]},
        {"heading": "Tool #2: GitHub Copilot", "body": "AI pair programmer that writes code 55% faster. Perfect for developers.", "captions": ["GitHub Copilot: AI pair programmer.", "Writes code 55% faster."]},
        {"heading": "Tool #3: Midjourney", "body": "Generate stunning images from text prompts. No design skills needed.", "captions": ["Midjourney: Generate stunning images from text.", "No design skills needed."]},
        {"heading": "The Results", "body": "Users report saving 10-20 hours per week. That's 500+ hours per year.", "captions": ["Users save 10-20 hours per week.", "That's 500+ hours per year."]},
        {"heading": "Get Started Today", "body": "All tools have free tiers. Start automating your workflow in minutes.", "captions": ["All tools have free tiers.", "Start automating in minutes."]},
        {"heading": "Why It Matters", "body": "AI is the biggest shift since the internet. Early adopters win the most.", "captions": ["AI is the biggest shift since the internet.", "Early adopters win the most."]},
        {"heading": "Pro Tips", "body": "Combine multiple AI tools for maximum productivity. Automate, delegate, eliminate.", "captions": ["Combine multiple AI tools for maximum productivity.", "Automate, delegate, eliminate."]},
        {"heading": "Key Takeaway", "body": "Start small. Pick one task to automate. Build from there. The future is AI.", "captions": ["Start small. Pick one task to automate.", "The future is AI."]},
    ]
    return random.sample(templates, min(count, len(templates)))

def create_slide_image(slide, index, width=1920, height=1080):
    """Create a slide image using Pillow"""
    if not HAS_PILLOW:
        return None
    
    img = Image.new('RGB', (width, height), '#0a0a1a')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Background gradient effect (simple)
    for y in range(height):
        r = int(10 + (y / height) * 20)
        g = int(10 + (y / height) * 15)
        b = int(26 + (y / height) * 40)
        for x in range(0, width, 4):
            draw.rectangle([x, y, x+3, y], fill=(r, g, b))
    
    # Accent line at top
    draw.rectangle([0, 0, width, 5], fill='#7c3aed')
    
    if slide["type"] == "title":
        # Title slide
        text = slide["text"]
        bbox = draw.textbbox((0, 0), text, font=font_title)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (width - tw) // 2
        y = (height - th) // 2 - 80
        draw.text((x, y), text, fill='#ffffff', font=font_title)
        
        sub = slide.get("subtitle", "")
        bbox2 = draw.textbbox((0, 0), sub, font=font_body)
        sw, sh = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        draw.text(((width - sw)//2, y + th + 30), sub, fill='#8888aa', font=font_body)
    
    elif slide["type"] == "content":
        # Content slide
        bullet = slide.get("bullet", "")
        title = f"#{bullet} {slide['title']}"
        draw.text((100, 100), title, fill='#7c3aed', font=font_title)
        
        # Body text with word wrap
        body = slide["text"]
        words = body.split()
        lines = []
        line = ""
        for word in words:
            test = line + " " + word if line else word
            bbox = draw.textbbox((0, 0), test, font=font_body)
            if bbox[2] - bbox[0] < width - 200:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        
        y = 250
        for line in lines:
            draw.text((100, y), line, fill='#ccccdd', font=font_body)
            y += 50
        
        # Bullet number badge
        draw.ellipse([width-120, 30, width-50, 100], fill='#7c3aed')
        draw.text((width-95, 45), str(bullet), fill='#ffffff', font=font_title)
    
    elif slide["type"] == "outro":
        text = slide["text"]
        bbox = draw.textbbox((0, 0), text, font=font_title)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((width-tw)//2, height//2-80), text, fill='#7c3aed', font=font_title)
        
        sub = slide.get("subtitle", "")
        bbox2 = draw.textbbox((0, 0), sub, font=font_body)
        sw, sh = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        draw.text(((width-sw)//2, height//2), sub, fill='#8888aa', font=font_body)
    
    # Footer
    draw.text((width-400, height-40), "AI Video Factory | ai-video-factory", fill='#444466', font=font_small)
    
    return img

def build_video(script, output_name=None):
    """Build MP4 video from script using ffmpeg"""
    if output_name is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = script["title"].lower().replace(" ", "-")[:40]
        output_name = f"{slug}_{ts}"
    
    work = OUTPUT_DIR / output_name
    work.mkdir(parents=True, exist_ok=True)
    
    # Generate slide images
    slide_files = []
    durations = []
    caption_lists = []
    
    for i, slide in enumerate(script["slides"]):
        img = create_slide_image(slide, i)
        if img:
            path = work / f"slide_{i:03d}.png"
            img.save(path)
            slide_files.append(str(path))
        else:
            # Fallback: create with ffmpeg drawtext
            path = work / f"slide_{i:03d}.png"
            text = slide.get("text", "Slide").replace("'", "'\\''")
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i",
                f"color=c=0x0a0a1a:s=1920x1080:d=1",
                "-vf", f"drawtext=text='{text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
                "-frames:v", "1", str(path)
            ], capture_output=True)
            slide_files.append(str(path))
        
        durations.append(slide.get("duration", 5))
        # Find matching captions
        caps = []
        for c in script.get("captions", []):
            if len(caps) < 2:
                caps.append(c)
        caption_lists.append(caps[:1] if caps else [])
    
    # Create SRT
    srt_path = work / "subtitles.srt"
    create_srt_proper(script, durations, srt_path)
    
    # Create concat file for slides
    concat_path = work / "concat.txt"
    with open(concat_path, 'w') as f:
        for sf, dur in zip(slide_files, durations):
            f.write(f"file '{sf}'\nduration {dur}\n")
    
    # Build video with ffmpeg
    output_video = work / f"{output_name}.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_path),
        "-vf", f"fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
        "-pix_fmt", "yuv420p",
        "-an",  # No audio
        str(output_video)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    
    if output_video.exists():
        size_mb = output_video.stat().st_size / (1024*1024)
        duration = sum(durations)
        return {
            "success": True,
            "video_path": str(output_video),
            "output_name": output_name,
            "size_mb": round(size_mb, 1),
            "duration_sec": duration,
            "slides": len(slide_files),
        }
    else:
        return {
            "success": False,
            "error": result.stderr[-500:],
        }

def create_srt_proper(script, durations, output_path):
    """Create proper SRT from captions"""
    srt = ""
    counter = 1
    time_pos = 0.0
    
    for i, (slide, dur) in enumerate(zip(script["slides"], durations)):
        caps = script.get("captions", [])
        # Distribute captions across slides
        start_idx = i * max(1, len(caps) // max(1, len(script["slides"])))
        end_idx = min((i + 1) * max(1, len(caps) // max(1, len(script["slides"]))), len(caps))
        
        for j in range(start_idx, end_idx):
            cap = caps[j] if j < len(caps) else ""
            if not cap:
                continue
            words = len(cap.split())
            cap_dur = min(dur / max(1, end_idx - start_idx), max(2, words * 0.3))
            
            start = time_pos
            end = start + cap_dur
            s = int(start); e = int(end)
            start_str = f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d},{int((start%1)*1000):03d}"
            end_str = f"{e//3600:02d}:{(e%3600)//60:02d}:{e%60:02d},{int((end%1)*1000):03d}"
            srt += f"{counter}\n{start_str} --> {end_str}\n{cap}\n\n"
            counter += 1
            time_pos = end
        
        if end_idx <= start_idx:
            time_pos += dur
    
    with open(output_path, 'w') as f:
        f.write(srt)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = None
    
    print(f"🎬 AI Video Factory")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Generate script
    script = generate_script(topic)
    print(f"📝 Topic: {script['title']}")
    print(f"📊 Slides: {len(script['slides'])}")
    
    # Build video
    result = build_video(script)
    
    if result["success"]:
        print(f"✅ Video built: {result['video_path']}")
        print(f"   Size: {result['size_mb']} MB")
        print(f"   Duration: {result['duration_sec']}s")
        print(f"   Slides: {result['slides']}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown')}")
