# teams/utils.py
import pandas as pd
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend required for Django
import matplotlib.pyplot as plt
import io
import base64
from django.db import models

# teams/utils.py
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

def generate_team_stats(team):
    cravings = team.get_recent_cravings().values(
        'user__username', 
        'timestamp', 
        'intensity'
    )
    
    df = pd.DataFrame(list(cravings))
    if df.empty:
        return None, None, None, None

    # Calculate compliance (intensity <= 2)
    df['compliant'] = df['intensity'] <= 2
    stats = df.groupby('user__username')['compliant'].agg(
        total_cravings='count',
        compliant_cravings='sum'
    ).reset_index()
    
    stats['compliance_rate'] = stats['compliant_cravings'] / stats['total_cravings']
    stats = stats.round({'compliance_rate': 2})
    
    # Generate chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        stats['user__username'], 
        stats['compliance_rate'],
        color=['#2ecc71' if rate > stats['compliance_rate'].mean() else '#e74c3c' 
               for rate in stats['compliance_rate']]
    )
    plt.ylabel('Compliance Rate', fontsize=12)
    plt.title(f'Team Compliance Rates: {team.name}', pad=20)
    plt.ylim(0, 1)
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.0%}',
                 ha='center', va='bottom')
    
    # Convert to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return stats.to_dict('records'), chart
