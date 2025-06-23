from datetime import datetime
import html
import re
import bleach


def validatePassword(password):
    '''
    Validate a password based on specific criteria:
    - Must be a string
    - Must be at least 8 characters long
    - Must contain at least one letter and one number
    - Must not exceed 255 character
    '''
    if not isinstance(password, str):
        return False
    if len(password) < 8:
        return False
    if not re.search(r"[a-zA-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if len(password) > 255:
        return False
    return True

def validateEmail(email):
    '''
    Validate an email address based on specific criteria:
    - Must be a string
    - Must match a specific regex pattern
    - Must not exceed 255 characters
    '''
    if not isinstance(email, str):
        return False
    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", email):
        return False
    if len(email) > 255:
        return False
    return True

def validateName(firstname, lastname):
    '''
    Validate a name based on specific criteria:
    - Both firstname and lastname must be strings
    - Each must not exceed 16 characters
    - Each must contain only alphabetic characters
    '''
    if not isinstance(firstname, str) or not isinstance(lastname, str):
        return False
    if len(firstname) > 16 or len(lastname) > 16:
        return False
    if not re.match(r"^[A-Za-z]+$", firstname) or not re.match(r"^[A-Za-z]+$", lastname):
        return False
    return True

def validateLog(title, body, due_date, label):
    '''
    Validate a log entry based on specific criteria:
    - Title must be a string and not exceed 64 characters
    - Body must be a string and not exceed 64 characters
    - Due date must be a string in the format 'YYYY-MM-DD' or None
    - Label must be a string and not exceed 64 characters
    '''
    if not isinstance(title, str):
        return False
    if len(title) > 64:
        return False
    if len(body) > 64:
        return False
    if due_date is not None:
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            return False
    if len(label) > 64:
        return False
    return True

def sanitizeQuery(query):
    '''
    Sanitize a query string to prevent SQL injection and XSS attacks:
    - Strips leading and trailing whitespace
    - Escapes special characters like %, _, and ;
    - Replaces them with their escaped versions
    - Limits the length to 255 characters
    '''
    query = query.strip()
    query = query.replace('%', r'\%').replace('_', r'\_')
    query = query.replace(';', '')
    query = html.escape(query)
    if len(query) > 255:
        return query[:255]
    return query

# TinyMCE already has sanitisation
def sanitizeLog(body):
    '''
    Sanitize the body of a log entry to prevent XSS attacks:
    - Uses bleach to allow only a specific set of HTML tags and attributes
    - Allows basic formatting tags like <p>, <br>, <span>, <div>, <strong>, <em>, <ul>, <ol>, <li>, <blockquote>, and <pre>
    '''
    allowed_tags = set(bleach.sanitizer.ALLOWED_TAGS)
    allowed_tags.update(['p', 'br', 'span', 'div', 'strong', 'em', 'ul', 'ol', 'li', 'blockquote', 'pre'])
    allowed_attributes = bleach.sanitizer.ALLOWED_ATTRIBUTES
    allowed_attributes.update({
        'span': [],
        'div': [],
        'p': [],
        'strong': [],
        'em': [],
        'ul': [],
        'ol': [],
        'li': [],
        'blockquote': [],
        'pre': [],
    })
    safe_body = bleach.clean(body, tags=allowed_tags, attributes=allowed_attributes)
    return safe_body
