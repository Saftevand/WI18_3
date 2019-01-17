'''

Remove user and movie bias R

Um = #Of movie ratings
Mu = #Of user ratings
N = #Of movie-user pairs

--Preprocessing R
Foreach Rmu in R
    Rmu = Rmu - 1/Um * SUM(Rms) - 1/Mu * SUM(Rru) + 1/N * SUM(Rsr)

--Compute singular value decomposition of R
U,S,V = R.svd()

--Compute User-factor and movie-factor matrices
A = matrixMult(U, sqrt(S))
B = matrixMult(sqrt(S), transpose(V))

--for stochastic gradient descent
for i in range(0, epochs)

    --Compute R_hat, from
    for m in Movies
        for u in Users
            for k in K
                R_hat[m,u] = matrixMult(Amk, Bku)

    --Compute error
    for m in Movies
        for u in Users
            Error = math.Pow((Rmu - R_hat_mu),2)

    --Compute error
    randu, randm = rand(R)
    Error = math.Pow((R[randm, randu] - R_hat_mu[randm, randu]),2)

    --Stochastic gradient descent
    for m in Movies
        for u in Users
            for k in K
                Amk = Amk + lr * Error * Bku
                Bku = Bku + lr * Amk * Error

--Final predictions
def predict(Movie, User)
    predictionScore = R_hat[Movie, User]

    --Account for bias
    predictionScore = predictionScore + 1/Um * SUM(Rms) + 1/Mu * SUM(Rru) - 1/N * SUM(Rsr)

    return predictionScore

'''