from importlib.resources import contents
from turtle import title
from typing import Any
from django.core.management.base import BaseCommand
from amazon.models import Post,Category
import random

class Command(BaseCommand):
    help="This command inserts data into the Post model"
    def handle(self,*args:Any,**options:Any):
        Post.objects.all().delete()
        titles=[
   "Apple iPhone 16 Pro",
   "Samsung Galaxy S25 Ultra",
   "Dell XPS 15 Laptop",
   "Apple MacBook Air M4",
   "Sony WH-1000XM5 Headphones",
   "Logitech MX Master 3S Mouse",
   "Nike Air Max Sneakers",
   "Adidas Running Shoes",
   "Men's Casual Cotton Shirt",
   "Women's Floral Dress",
   "Modern Wooden Study Table",
   "Luxury Office Chair",
   "Smart LED TV 55-inch",
   "Canon EOS R10 Camera",
   "Kitchen Mixer Grinder",
   "Air Fryer XL",
   "Smart Fitness Watch",
   "Bluetooth Portable Speaker",
   "Gaming Mechanical Keyboard",
   "PlayStation 5 Console"
]
        contents=[
    "Experience unmatched speed, stunning photography, and all-day battery life with Apple's latest flagship smartphone.",
    "Enjoy AI-powered features, a vibrant AMOLED display, and professional-grade cameras for an exceptional mobile experience.",
    "A premium laptop designed for productivity, creativity, and entertainment with powerful performance and a brilliant display.",
    "Ultra-lightweight and incredibly fast, this laptop offers outstanding battery life and seamless performance for work and study.",
    "Immerse yourself in crystal-clear audio with industry-leading noise cancellation and exceptional comfort.",
    "Boost your productivity with precise tracking, silent clicks, and customizable controls for effortless multitasking.",
    "Designed for comfort and style, these sneakers provide superior cushioning for daily wear and athletic activities."
    "Lightweight running shoes with breathable materials and responsive cushioning for maximum comfort and performance.",
    "A stylish cotton shirt that offers exceptional comfort and a modern fit, perfect for casual and formal occasions.",
    "An elegant floral dress crafted from soft, breathable fabric, making it ideal for everyday wear and special events.",
    "A durable wooden study table with a spacious work surface, perfect for studying, working, or organizing your workspace.",
    "Ergonomically designed with adjustable height and lumbar support to provide maximum comfort during long working hours.",
    "Enjoy breathtaking 4K picture quality, smart streaming features, and immersive audio for an outstanding entertainment experience.",
    "Capture stunning photos and cinematic videos with fast autofocus, high-resolution imaging, and advanced shooting features.",
    "A powerful kitchen appliance that makes grinding, blending, and mixing quick, easy, and efficient for everyday cooking.",
    "Prepare crispy and delicious meals with little to no oil while maintaining great taste and healthier cooking.",
    "Monitor your heart rate, sleep, daily activities, and workouts while staying connected with smart notifications.",
    "Enjoy rich, powerful sound with a compact wireless speaker that's perfect for travel, parties, and outdoor adventures.",
    "Experience faster response times, tactile mechanical switches, and customizable RGB lighting for an enhanced gaming setup.",
    "Discover next-generation gaming with ultra-fast performance, realistic graphics, and an exciting collection of exclusive games."
]
        img_urls=[
    "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600",
    "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600",
    "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600",
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
    "https://images.unsplash.com/photo-1527814050087-3793815479db?w=600",
    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600",
    "https://images.unsplash.com/photo-1543508282-6319a3e2621f?w=600",
    "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600",
    "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600",
    "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=600",
    "https://images.unsplash.com/photo-1505843513577-22bb7d21e455?w=600",
    "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=600",
    "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600",
    "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=600",
    "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=600"
    "https://images.unsplash.com/photo-1507874457470-272b3c8d8ee2?w=600",
    "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=600",
    "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600"
]
        categories=Category.objects.all()
        for title,content,img_url in zip(titles,contents,img_urls):
            category=random.choice(categories)
            Post.objects.create(title=title, content=content, img_url=img_url, category=category)
        
        self.stdout.write(self.style.SUCCESS("Data inserted successfully!"))

