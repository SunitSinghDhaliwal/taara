# Taara – Aapki India Se Dost

**Great Indian AI Internship Challenge by Gnani AI**
Sunit Singh Dhaliwal, Thapar Institute of Engineering and Technology

## The problem
Millions of Indian kids grow up abroad. They love their Dadi, Nani, Bua and Chacha back home, but most can't hold a conversation in Hindi or Punjabi. Family calls turn into "yes Dadi", "good", "okay", and then the phone gets passed back to a parent. Language apps teach vocabulary, not how to actually talk to your grandmother.

## Who it's for
- NRI kids aged 2 to 10 (games for ages 2 to 4 need no speaking)
- Parents who want their kids to stay connected to family and language

## The solution
Taara is a practice buddy that gets kids ready for real family calls.

- **Pretend call (main feature):** the kid picks a relative (Dadi, Dada, Nani, Nana, Bua, Chacha, Mausi, Mama, or Bebe, Bhua, Masi in Punjabi). Taara plays that relative and talks in simple Hindi or Punjabi. The kid replies by voice. If they answer in English, Taara shows how to say it in Hindi and they try again.
- **Phrases for the call:** learn what each relative usually asks and how to answer, with stars, XP and a build-the-sentence bonus.
- **Say it in Hindi:** type or say anything in English and hear it in Hindi.
- **Little ones:** Find the colour, Count with Taara, Listen and learn.
- **For parents:** progress view, a WhatsApp summary, and the option to add family phrases.

Taara never pretends to be real family outside clearly announced pretend games, and every session ends by pointing the kid to a real call.

## Gnani AI stack
- **Gnani Prisma v3.0 (speech to text, REST):** turns the child's speech into text so Taara can check their Hindi and reply.
- **Gnani Timbre v3.0 (text to speech):** voices for every character. Lakshmi for Taara and female relatives, Yashraj for male relatives.

Other parts: FastAPI backend with a single web page; Groq (gpt-oss-120b) for replies, translation and grading, with guardrails (script check, child-safe topics, no personal details).

## Impact
Kids get a safe place to make mistakes before the real call. Grandparents get grandkids who can actually talk to them. The same approach can work for any Indian language Gnani supports.

## Limits and next steps
Not yet tested with real children, and Prisma is tuned for adult voices. Next: test with families, add more languages, and add a mobile app.
