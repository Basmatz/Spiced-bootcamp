import pandas as pd

spices = ['One-Hot Chili Peppers',
          'Bayesian Basil',
          'Tensor Thyme',
          'Linear Lavender',
          'Artificial Neural Nutmeg',
          'Polynomial Peppermint',
          'Sigmoid Saffron'
          ]
participants = [2, 6, 9, 9, 9, 8,5]

df = pd.DataFrame({'name': spices,
                   'participants': participants
                   })

print(df.sort_values(by='participants', ascending=False))

print("\ntotal participants:", df['participants'].sum())