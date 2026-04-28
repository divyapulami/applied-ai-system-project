# Knowledge base for the RAG system.
# Organized by species → breed-specific facts.
# The retriever searches by species, breed name, and life stage.

PET_CARE_KNOWLEDGE = [

    # ──────────────────────────────────────────
    # GENERAL DOG FACTS (apply to all dogs)
    # ──────────────────────────────────────────
    "Dogs need fresh clean water available at all times.",
    "Puppies under 6 months need to eat 3 to 4 times a day.",
    "Adult dogs should be fed two times a day, morning and evening.",
    "Senior dogs over 8 years old need shorter, gentler walks to protect their joints.",
    "All dogs need annual vet checkups and vaccinations.",
    "Dogs should be given flea and tick prevention every 1 to 3 months.",
    "Dogs need their nails trimmed every 3 to 4 weeks.",
    "Puppies need vaccinations starting at 6 to 8 weeks old.",

    # ──────────────────────────────────────────
    # DOG BREEDS
    # ──────────────────────────────────────────

    # Labrador Retriever
    "Labrador Retriever needs at least 60 minutes of vigorous exercise every day to stay healthy.",
    "Labrador Retriever loves swimming and fetching — these are great ways to exercise them.",
    "Labrador Retriever is prone to obesity so avoid overfeeding and limit treats.",
    "Labrador Retriever sheds heavily and needs brushing 2 to 3 times a week.",
    "Labrador Retriever is prone to hip dysplasia, so regular vet checkups are important.",

    # Golden Retriever
    "Golden Retriever needs 60 to 90 minutes of exercise per day including walks and play.",
    "Golden Retriever has a thick double coat and needs brushing at least 3 times a week.",
    "Golden Retriever is prone to ear infections — check and clean ears weekly.",
    "Golden Retriever loves to carry things in its mouth — fetch games are great for mental stimulation.",
    "Golden Retriever is prone to cancer, so yearly vet checkups after age 5 are very important.",

    # German Shepherd
    "German Shepherd needs 60 to 90 minutes of exercise daily and loves having a job to do.",
    "German Shepherd sheds year-round and needs daily brushing to manage loose fur.",
    "German Shepherd is prone to hip and elbow dysplasia — avoid over-exercising puppies.",
    "German Shepherd needs early socialization and training to prevent anxiety or aggression.",
    "German Shepherd thrives with mental challenges like puzzle toys and obedience training.",

    # French Bulldog
    "French Bulldog only needs 20 to 30 minutes of light exercise per day.",
    "French Bulldog cannot tolerate heat — never exercise them in hot weather or direct sun.",
    "French Bulldog is prone to breathing problems due to its flat face — avoid strenuous activity.",
    "French Bulldog needs their facial skin folds cleaned weekly to prevent infections.",
    "French Bulldog is prone to allergies — watch for itchy skin and discuss diet with your vet.",

    # Poodle
    "Poodle needs 40 to 60 minutes of exercise per day and loves swimming and agility.",
    "Poodle has a curly coat that does not shed much but needs professional grooming every 6 to 8 weeks.",
    "Poodle is highly intelligent and needs daily mental stimulation through training and puzzle toys.",
    "Poodle is prone to ear infections due to hair growing inside the ear canal — clean ears regularly.",
    "Poodle comes in three sizes: standard, miniature, and toy — care needs vary slightly by size.",

    # Chihuahua
    "Chihuahua only needs 20 to 30 minutes of exercise per day — short walks are enough.",
    "Chihuahua is sensitive to cold weather and may need a sweater in winter.",
    "Chihuahua is prone to dental disease — brush their teeth 3 times a week.",
    "Chihuahua can be fragile — handle gently and keep away from rough play with large dogs.",
    "Chihuahua tends to bond strongly with one person and can become anxious around strangers.",

    # Beagle
    "Beagle needs 60 minutes of exercise per day and loves sniffing and exploring outdoors.",
    "Beagle has a strong scent drive and should always be walked on a leash or in a fenced area.",
    "Beagle is prone to obesity — measure food portions carefully and avoid excess treats.",
    "Beagle ears hang low and need weekly cleaning to prevent ear infections.",
    "Beagle can be vocal and howl if left alone too long — needs company and stimulation.",

    # Husky
    "Husky needs 2 hours of vigorous exercise every day — they are a very high-energy breed.",
    "Husky has a thick double coat and sheds heavily twice a year — brush daily during shedding season.",
    "Husky can overheat easily — avoid exercise in hot weather and always provide shade and water.",
    "Husky is an escape artist — needs a securely fenced yard with no gaps.",
    "Husky is prone to eye problems like cataracts — annual eye checkups are recommended.",

    # Shih Tzu
    "Shih Tzu only needs 20 to 30 minutes of light exercise per day.",
    "Shih Tzu has a long silky coat that needs brushing every day to prevent tangles.",
    "Shih Tzu needs professional grooming or a short 'puppy cut' every 6 to 8 weeks.",
    "Shih Tzu has a flat face and can have breathing difficulties in heat — keep them cool.",
    "Shih Tzu is prone to eye infections — wipe around the eyes daily with a damp cloth.",

    # Dachshund
    "Dachshund needs 30 to 45 minutes of moderate exercise per day.",
    "Dachshund has a long spine and is prone to back problems — never let them jump off furniture.",
    "Dachshund should use ramps or stairs instead of jumping to protect their back.",
    "Dachshund loves to dig and follow scents — secure your garden fence.",
    "Dachshund can be stubborn — consistent positive reinforcement training works best.",

    # Border Collie
    "Border Collie needs at least 2 hours of intense exercise every day — they are extremely high energy.",
    "Border Collie is one of the most intelligent dog breeds and needs constant mental stimulation.",
    "Border Collie thrives with agility training, frisbee, and herding activities.",
    "Border Collie can develop anxiety or destructive behavior if not given enough exercise and mental work.",
    "Border Collie coat needs brushing 2 to 3 times a week to prevent matting.",

    # ──────────────────────────────────────────
    # GENERAL CAT FACTS (apply to all cats)
    # ──────────────────────────────────────────
    "All cats need fresh clean water every day — some cats prefer a pet water fountain.",
    "Adult cats should be fed two times a day, morning and evening.",
    "Kittens under 6 months need to eat 3 to 4 times a day.",
    "All cats need their litter box scooped daily and fully cleaned once a week.",
    "All cats need annual vet checkups and vaccinations.",
    "Cats need a scratching post to keep their claws healthy.",
    "Indoor cats need toys and play sessions to stay mentally stimulated.",

    # ──────────────────────────────────────────
    # CAT BREEDS
    # ──────────────────────────────────────────

    # Persian
    "Persian cat has a very long thick coat that needs brushing every single day to prevent matting.",
    "Persian cat needs professional grooming every 4 to 6 weeks.",
    "Persian cat has a flat face and is prone to breathing difficulties and eye discharge — wipe eyes daily.",
    "Persian cat is calm and gentle — they prefer a quiet indoor environment.",
    "Persian cat is prone to kidney disease — annual vet bloodwork is recommended after age 4.",

    # Siamese
    "Siamese cat is very vocal and will meow loudly to communicate — be prepared for a chatty cat.",
    "Siamese cat is extremely social and can suffer from loneliness if left alone for long periods.",
    "Siamese cat has a short coat that needs brushing only once a week.",
    "Siamese cat is prone to dental disease — brush their teeth weekly.",
    "Siamese cat loves interactive play and puzzle feeders to keep their sharp mind busy.",

    # Maine Coon
    "Maine Coon is one of the largest domestic cat breeds and needs more food than average cats.",
    "Maine Coon has a thick semi-long coat that needs brushing 2 to 3 times a week.",
    "Maine Coon loves water and may try to splash in their water bowl.",
    "Maine Coon is prone to hip dysplasia and heart disease — annual vet checkups are important.",
    "Maine Coon is dog-like in personality and can be trained to walk on a leash.",

    # Bengal
    "Bengal cat is extremely active and needs at least 30 to 45 minutes of active play every day.",
    "Bengal cat loves to climb — provide tall cat trees and wall shelves.",
    "Bengal cat has a short spotted coat that needs minimal grooming — brush once a week.",
    "Bengal cat is very intelligent and can learn to open doors and drawers.",
    "Bengal cat can be destructive if bored — rotate toys and provide constant stimulation.",

    # Ragdoll
    "Ragdoll cat is very gentle and goes limp when held — they love being carried.",
    "Ragdoll cat has a semi-long silky coat that needs brushing 2 times a week.",
    "Ragdoll cat is prone to heart disease — ask your vet about annual heart scans.",
    "Ragdoll cat is an indoor-only breed and should never be let outside unsupervised.",
    "Ragdoll cat is very social and gets along well with children and other pets.",

    # British Shorthair
    "British Shorthair is calm and independent — they enjoy company but don't demand attention.",
    "British Shorthair has a dense plush coat that needs brushing twice a week.",
    "British Shorthair is prone to obesity — measure food carefully and encourage play.",
    "British Shorthair is prone to heart disease — annual vet checkups are recommended.",
    "British Shorthair adapts well to apartment living and doesn't need much space.",

    # Sphynx
    "Sphynx cat has no fur and needs weekly baths to remove oil buildup on their skin.",
    "Sphynx cat gets cold easily and may need a cat sweater in cool weather.",
    "Sphynx cat ears accumulate wax quickly and need cleaning every week.",
    "Sphynx cat is very social and affectionate — they hate being left alone.",
    "Sphynx cat is prone to heart disease — annual cardiac checkups are strongly recommended.",

    # ──────────────────────────────────────────
    # RABBIT BREEDS
    # ──────────────────────────────────────────

    # General rabbit facts
    "All rabbits need unlimited fresh hay every day — it should make up 80% of their diet.",
    "All rabbits need fresh leafy greens like romaine lettuce and kale daily.",
    "All rabbits should never be fed iceberg lettuce, chocolate, or avocado — these are toxic.",
    "All rabbits need at least 3 hours of free roaming time outside their cage every day.",
    "All rabbits need annual vet checkups with a vet who specializes in small animals.",
    "All rabbits should be spayed or neutered to prevent reproductive cancers.",

    # Holland Lop
    "Holland Lop is a small rabbit that weighs around 2 to 4 pounds.",
    "Holland Lop has floppy ears that need weekly cleaning to prevent ear infections.",
    "Holland Lop is gentle and social — they enjoy being held and petted.",
    "Holland Lop needs daily brushing during shedding season to manage loose fur.",

    # Lionhead
    "Lionhead rabbit has a distinctive fluffy mane of fur around its head.",
    "Lionhead rabbit needs daily brushing of their mane to prevent matting.",
    "Lionhead rabbit is energetic and curious — provide plenty of toys and tunnels.",
    "Lionhead rabbit can be shy at first but bonds strongly with their owner over time.",

    # Flemish Giant
    "Flemish Giant is one of the largest rabbit breeds and can weigh over 14 pounds.",
    "Flemish Giant needs a very large enclosure — at least 3 feet by 4 feet minimum.",
    "Flemish Giant needs more food than smaller breeds due to their large size.",
    "Flemish Giant is gentle and calm despite their large size — great for families.",
    "Flemish Giant is prone to sore hocks from sitting on hard surfaces — use soft bedding.",

    # Mini Rex
    "Mini Rex has an incredibly soft velvety coat that needs minimal grooming — brush once a week.",
    "Mini Rex is playful and curious — they love exploring and playing with toys.",
    "Mini Rex is a good beginner rabbit breed due to their calm and friendly nature.",

    # ──────────────────────────────────────────
    # GUINEA PIG
    # ──────────────────────────────────────────
    "Guinea pig needs fresh hay available at all times — it is essential for their digestion.",
    "Guinea pig needs fresh vegetables like bell peppers and leafy greens every day.",
    "Guinea pig requires vitamin C in their diet — they cannot produce it on their own.",
    "Guinea pig is a social animal and should never be kept alone — get at least two.",
    "Guinea pig needs their cage cleaned at least twice a week to stay healthy.",
    "Guinea pig long-haired breeds like Peruvian need daily brushing.",
    "Guinea pig nails need trimming every 4 to 6 weeks.",

    # ──────────────────────────────────────────
    # HAMSTER
    # ──────────────────────────────────────────
    "Hamster is nocturnal and is most active at night — avoid disturbing them during the day.",
    "Hamster needs a wheel of at least 8 inches in diameter to run safely.",
    "Hamster cage needs cleaning once a week to prevent odor and disease.",
    "Hamster needs fresh water from a bottle changed every day.",
    "Hamster cheek pouches can get impacted — avoid sticky foods like peanut butter.",
    "Syrian hamster must be kept alone — they are solitary and will fight other hamsters.",
    "Dwarf hamster can sometimes live in pairs if introduced from a young age.",

    # ──────────────────────────────────────────
    # PARROT / BIRD
    # ──────────────────────────────────────────
    "Parrot needs several hours of social interaction outside the cage every day.",
    "Parrot needs a balanced diet of pellets, fresh fruit, and vegetables.",
    "Parrot should never be fed avocado, chocolate, or caffeine — these are toxic to birds.",
    "Parrot cage needs cleaning every day to prevent bacterial infections.",
    "Parrot needs mental stimulation through toys, foraging, and training sessions.",
    "Budgie is a small parrot that is great for beginners — they are gentle and easy to care for.",
    "Cockatiel is a friendly parrot breed that loves being petted on the head and cheeks.",
    "African Grey parrot is extremely intelligent and can learn hundreds of words.",

]
