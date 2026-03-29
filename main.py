import hashlib
import re
from datetime import datetime

class AlemTrustEngine:
    def __init__(self):
 
        self.fraud_patterns = {
            "guarantee_risk": ["100%", "кепілдік", "гарантия", "результат"],
            "speed_risk": ["ускорение", "тез арада", "очередьсіз", "вход", "доступ"],
            "middleman_risk": ["помощь в подаче", "көмектесеміз", "байланыс", "свои люди"]
        }

    def _calculate_risk_score(self, text):
        """Қауіп деңгейін есептеу логикасы (Risk Scoring)"""
        found_matches = []
        score = 0
        
        for category, patterns in self.fraud_patterns.items():
            for pattern in patterns:
                if pattern in text.lower():
                    found_matches.append(pattern)
                    score += 25 

        return min(score, 100), found_matches

    def _validate_iin(self, text):
        """Мәтін ішінен ИИН тауып, оның форматын тексеру"""
        iin_pattern = r'\b\4\b' 
        iin_match = re.search(r'\d{12}', text)
        if iin_match:
            iin = iin_match.group(0)
           
            return f"✅ ИИН табылды: {iin}"
        return "⚠️ ИИН табылмады немесе форматы қате."

    def analyze_document(self, raw_text):
        """Негізгі анализ функциясы"""
        print(f"--- AlemTrust AI: Аудит басталды ---")
        
        
        fingerprint = hashlib.sha256(raw_text.encode()).hexdigest()
        
        risk_percent, matches = self._calculate_risk_score(raw_text)
        
        iin_status = self._validate_iin(raw_text)
        
        
        summary = "Құжатта делдалдық қызметтердің белгілері бар. Ресми органдарға жүгіну ұсынылады." if risk_percent > 30 else "Құжат ресми стандарттарға сай келеді."

        results = {
            "document_hash": fingerprint,
            "risk_score": f"{risk_percent}%",
            "detected_patterns": matches,
            "data_validation": iin_status,
            "ai_conclusion": summary
        }
        
        return results

if __name__ == "__main__":
    engine = AlemTrustEngine()
    test_text = "Мен, Ахметов А., 850101300123. Кезексіз тез арада анықтама алуға көмектесемін, 100% кепілдік."
    
    report = engine.analyze_document(test_text)
    
    for key, value in report.items():
        print(f"{key.upper()}: {value}")