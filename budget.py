class Category:

  def __init__(self, label):
    self.label = label
    self.ledger = []

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  def get_balance(self):
    return sum(map(lambda entry: entry["amount"], self.ledger))

  def transfer(self, amount, budget):
    if self.withdraw(amount, "Transfer to " + budget.label):
      budget.deposit(amount, "Transfer from " + self.label)
      return True
    return False

  def check_funds(self, amount):
    return amount <= self.get_balance()

  def get_withdrawals(self):
    withdraw_operations = filter(lambda entry: entry["amount"] < 0,
                                 self.ledger)
    total_withdrawals = abs(
        sum(map(lambda entry: entry["amount"], withdraw_operations)))
    return total_withdrawals

  def __str__(self):
    # Format title
    formatted_title = self.label.center(30, '*')
    # Format historical
    formatted_entries = map(
        lambda entry: f"{entry['description'][:23]:23}{entry['amount']:>7.2f}",
        self.ledger)
    formatted_historical = "\n".join(formatted_entries)
    # format balance
    formatted_balance = f"Total: {self.get_balance():.2f}"
    return f"{formatted_title}\n{formatted_historical}\n{formatted_balance}"


def create_spend_chart(categories):
  template_string = "Percentage spent by category\n"
  # Calculate total withdrawals for each budget
  total_withdrawals = list(
      map(lambda category: category.get_withdrawals(), categories))
  # Calculate total of all withdrawals for each budget
  total = sum(total_withdrawals)
  # Calculate a list of percentages for each withdrawal total
  percentages = list(map(lambda withdrawal: withdrawal / total * 100, total_withdrawals))
  concepts = list(map(lambda category: category.label, categories))
  # Find the maximum length of all words
  max_length = max(len(label) for label in concepts)
  for percent in range(100, -10, -10):
    chart_entries = list(
        map(lambda per: 'o' if per >= percent else ' ', percentages))
    # Set a format for teh chart
    template_string += f"{'{0}| '.format(percent).rjust(5)}{'  '.join(chart_entries)}  \n"
  # Separator
  template_string += f"{'':4}-{'--'.join(['-']*len(percentages))}--\n"
  # Add the concepts labels for each budget
  labels = list(zip(*(label.ljust(max_length) for label in concepts)))
  template_string += '\n'.join([' ' * 5 + '  '.join(col) + ' '*2 for col in labels])
  return template_string
