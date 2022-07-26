# p6_model_train_cbf_cbow
# # Get binary encoding
    # digit = math.ceil(math.log(len(label_encoding), 2))
    # encoding = [0] * digit
    # for key in label_encoding.keys():
    #     i = digit-1
    #     breaking = False
    #     while((not breaking)):
    #         if encoding[i] == 0 or i == 0: breaking = True
    #         encoding[i] = (encoding[i] + 1) % 2
    #         i -= 1
    #     label_encoding[key] = encoding.copy()