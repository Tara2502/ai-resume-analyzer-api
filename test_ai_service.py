from app.services.ai_service import analyze_resume


tes_resume="""
Tara is a java developer with experience in backend development.
Skills:
Java,Spring Boot, Hibernate, PostgresSQL, React

Experience: Software Engineer working on REST APIs backend applications.
"""

result = analyze_resume(tes_resume)

print("SUMMARY:")
print(result.summary)

print("\nSKILLS:")
print(result.skills)

print("\nSTRENGTHS:")
print(result.strengths)

print("\nWEAKNESSES:")
print(result.weaknesses)

print("\nSUGGESTIONS:")
print(result.suggestions)