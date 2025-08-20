def main():
    """
    Data processing example with lists and dictionaries
    """
    # Sample data
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    
    # Process data
    even_numbers = [n for n in numbers if n % 2 == 0]
    odd_numbers = [n for n in numbers if n % 2 != 0]
    name_lengths = {name: len(name) for name in names}
    
    # Calculate statistics
    total_sum = sum(numbers)
    average = total_sum / len(numbers)
    
    result = {
        "original_numbers": numbers,
        "even_numbers": even_numbers,
        "odd_numbers": odd_numbers,
        "name_lengths": name_lengths,
        "statistics": {
            "total_sum": total_sum,
            "average": average,
            "count": len(numbers)
        }
    }
    
    return result
