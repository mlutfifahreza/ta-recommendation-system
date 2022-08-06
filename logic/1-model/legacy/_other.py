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

def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))

def activate(inputs, weights):
    result = []
    for w in weights:
        result.append(sigmoid(np.dot(inputs, w)))
    return np.array(result)

def error(outputs, targets):
    return np.square(np.subtract(targets, outputs)).mean()

# plot final inputs - centroids
plt.scatter(np.take(inputs, indices=0, axis=1), np.take(inputs, indices=1, axis=1), c=rgb_black)
plt.scatter(np.take(centroids, indices=0, axis=1), np.take(centroids, indices=1, axis=1), c=rgb_red)
plt.title('inputs - centroids')
save_path = '/result/fcm.png'
plt.savefig(save_path, bbox_inches='tight')
os.system(f'open {save_path}')