from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv('grouped_pitches.csv')

def find_similar_pitches(input_pitch):
    df['distance'] = np.sqrt(
        (df['release_speed'] - input_pitch['release_speed'])**2 +
        (df['pfx_x'] - input_pitch['pfx_x'])**2 +
        (df['pfx_z'] - input_pitch['pfx_z'])**2 +
        (df['release_spin_rate'] - input_pitch['release_spin_rate'])**2 +
        (df['release_extension'] - input_pitch['release_extension'])**2
    )
    
    similar_pitches = df.nsmallest(5, 'distance')
    return similar_pitches.to_html(classes='table table-striped', index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    similar_pitches = None
    if request.method == 'POST':
        input_pitch = {
            'release_speed': float(request.form.get('release_speed')),
            'pfx_x': float(request.form.get('pfx_x')),
            'pfx_z': float(request.form.get('pfx_z')),
            'release_spin_rate': float(request.form.get('release_spin_rate')),
            'release_extension': float(request.form.get('release_extension'))
        }
        similar_pitches = find_similar_pitches(input_pitch)
    
    return render_template('index.html', similar_pitches=similar_pitches)

if __name__ == '__main__':
    app.run(debug=True)
