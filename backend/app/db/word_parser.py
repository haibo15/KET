import re
from typing import List, Dict, Optional, Tuple

class WordParser:
    def __init__(self):
        self.current_topic = None
        self.words_by_topic = {}
        
    def parse_part_of_speech(self, text: str) -> List[str]:
        """解析词性标记"""
        pos_pattern = r'\((adj|adv|n|v|phr v|det|pron|prep|conj|art|n pl|exclam)\)'
        matches = re.findall(pos_pattern, text)
        return matches if matches else []
    
    def parse_word_line(self, line: str) -> Optional[Dict]:
        """解析单个单词行"""
        # 跳过空行和标题行
        if not line.strip() or line.startswith('#') or line.startswith('**'):
            return None
            
        # 基本解析
        parts = line.strip().split('**(')
        if len(parts) < 2:
            return None
            
        word = parts[0].strip()
        pos_parts = parts[1].split(')**')
        pos = pos_parts[0]  # 词性
        
        # 提取例句
        examples = []
        if len(pos_parts) > 1 and '-' in pos_parts[1]:
            examples = [ex.strip() for ex in pos_parts[1].split('-') if ex.strip()]
        
        return {
            "word": word,
            "part_of_speech": pos,
            "examples": examples,
            "topic_categories": [self.current_topic] if self.current_topic else [],
            "difficulty_level": "A"  # 默认难度级别
        }
    
    def parse_topic_section(self, text: str) -> Dict[str, List[Dict]]:
        """解析主题分类下的单词"""
        lines = text.strip().split('\n')
        words = []
        
        for line in lines:
            if line.startswith('**') and ':' in line:
                # 新主题开始
                self.current_topic = line.strip('*').strip().split(':')[0].strip()
                continue
                
            word_data = self.parse_word_line(line)
            if word_data:
                words.append(word_data)
                
        return words
    
    def parse_topic_table(self, table_text: str) -> List[Dict]:
        """解析主题表格中的单词"""
        words = []
        lines = table_text.strip().split('\n')
        
        for line in lines:
            if '|' not in line or line.startswith('|:-'):
                continue
                
            # 分割表格行
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            for cell in cells:
                if not cell or cell.startswith('**'):
                    continue
                    
                # 解析单词和词性
                match = re.match(r'([^\(]+)(?:\s*\(([^\)]+)\))?', cell)
                if match:
                    word, pos = match.groups()
                    words.append({
                        "word": word.strip(),
                        "part_of_speech": pos if pos else "n",  # 默认为名词
                        "topic_categories": [self.current_topic] if self.current_topic else [],
                        "difficulty_level": "A"
                    })
        
        return words
    
    def parse_file(self, content: str) -> List[Dict]:
        """解析整个文件内容"""
        all_words = []
        
        # 分割文件为主要部分
        sections = content.split('# ')
        
        for section in sections:
            if not section.strip():
                continue
                
            # 解析主题分类下的单词
            words = self.parse_topic_section(section)
            all_words.extend(words)
            
            # 解析主题表格
            if '|' in section:
                table_words = self.parse_topic_table(section)
                all_words.extend(table_words)
        
        return all_words 