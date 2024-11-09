from decoder.decoder import Decoder

if __name__ == "__main__":
    decoder = Decoder("data.txt", "output.txt")
    decoder.decode()
    decoder.show_maps()
    decoder.recursive_descent()
    # decoder.operator_precedence()