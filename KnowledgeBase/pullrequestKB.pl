:- use_module(library(csv)).

read_dataset(FileName) :-
	csv_read_file(FileName , Data),
	assert_variables(Data).

assert_variables(Dataset) :-
	Dataset = [Row | Tail],
	Row = row(Project_Name, Owner, Name, Closer, Requester, Pull_Request_id, Github_id, Social_Distance, Num_comments, Prior_Interaction, Followers_Current, Age_Current, Test_File, Total_Churn, Files_Changed, Stars_Current, Team_Size, Main_Team_Member, Opennessx, Conscientiousnessx, Extraversionx, Agreeablenessx, Neuroticismx, Opennessy, Conscientiousnessy, Extraversiony, Agreeablenessy, Neuroticismy, Diff_openness_abs, Diff_conscientiousness_abs, Diff_extraversion_abs, Diff_agreeableness_abs, Diff_neuroticism_abs, Accepted),
	assert(project(Project_Name, Owner, Name, Pull_Request_id)),
	assert(closer(Closer, Pull_Request_id, Opennessx, Conscientiousnessx, Extraversionx, Agreeablenessx, Neuroticismx)),
	assert(requester(Requester, Pull_Request_id, Opennessy, Conscientiousnessy, Extraversiony, Agreeablenessy, Neuroticismy)),
	assert(pullrequest(Closer, Requester, Pull_Request_id, Social_Distance, Num_comments, Prior_Interaction, Followers_Current, Age_Current, Test_File, Total_Churn, Files_Changed, Stars_Current, Team_Size, Main_Team_Member, Diff_openness_abs, Diff_conscientiousness_abs, Diff_extraversion_abs, Diff_agreeableness_abs, Diff_neuroticism_abs, Accepted)),
	assert_variables(Tail).

assert_variables([]).

developer(Name) :-
	is_closer(Name),
	closer(Name, _, Opennessx, Conscientiousnessx, Extraversionx, Agreeablenessx, Neuroticismx),
	format('Developer: ~w', [Name]), nl,
	format('Openness: ~w', [Opennessx]), nl,
	format('Conscientiousness: ~w', [Conscientiousnessx]), nl,
	format('Extraversion: ~w', [Extraversionx]), nl,
	format('Agreeableness: ~w', [Agreeablenessx]), nl,
	format('Neuroticism: ~w', [Neuroticismx]), nl,
	list_pullrequest(Name).	

developer(Name) :-
	is_requester(Name),
	requester(Name, _, Opennessy, Conscientiousnessy, Extraversiony, Agreeablenessy, Neuroticismy),
	format('Developer: ~w', [Name]), nl,
	format('Openness: ~w', [Opennessy]), nl,
	format('Conscientiousness: ~w', [Conscientiousnessy]), nl,
	format('Extraversion: ~w', [Extraversiony]), nl,
	format('Agreeableness: ~w', [Agreeablenessy]), nl,
	format('Neuroticism: ~w', [Neuroticismy]), nl,
	list_pullrequest(Name).	

list_pullrequest(Name) :-
	is_closer(Name),
	pullrequest(Name, _, Pull_Request_id, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, Accepted),
	format('Pull Request : ~w ', Pull_Request_id). 

list_pullrequest(Name) :-
	is_requester(Name),
	pullrequest(_, Name, Pull_Request_id, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, Accepted),
	format('Pull Request : ~w ', Pull_Request_id). 

is_closer(X) :-
	closer(X, _, _, _, _, _, _).

is_requester(X) :-
	requester(X, _, _, _, _, _, _).

is_developer(X) :-
	closer(X, _, _, _, _, _, _).

is_developer(X) :-
	requester(X, _, _, _, _, _, _).

is_accepted(IdPullRequest) :-
	pullrequest(_, _, IdPullRequest, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, Accepted),
	Accepted is 1.

has_filetest(Name) :-
	pullrequest(_, _, Name, _, _, _, _, _, TestFile, _, _, _, _, _, _, _, _, _, _, _),
	TestFile is 1.

worked_together(Name1,Name2) :-
	closer(Name1, X, _, _, _, _, _),
	requester(Name2, X, _, _, _, _, _).

worked_together(Name1,Name2) :-
	closer(Name2, X, _, _, _, _, _),
	requester(Name1, X, _, _, _, _, _).



%In base ai test effettuati con k means possiamo affermare che se [Conscientiousness.x, Conscientiousness.y]
%sono vicini al centroide [0.2329318;  0.26503104] la pull request ha una probabilità di accettazione bassa.
%In base agli elementi del cluster in questione definiamo l'intervallo [0.2329318 +/- 0.20, 0.26503104 +/- 0.20] 
%se invece [Extraversion.x, Extraversion.y] molto vicini a [0.05763253 0.27890639] con intervallo [0.05763253 +/- 0.05, 0.27890639 +/- 0.05] e [Agreeableness.x, 
%Agreablenness.y] molto vicini a [0.02156959 0.35773928] c'è alta probabilità di accettazione con intervallo [0.02156959 +/- 0.02, 0.35773928 +/- 0.02]

inRange(I, J, K) :- K > I, K < J.

%case positive
might_work_well(NameCloser, NameRequester) :-
	closer(NameCloser, _, Opennessx, Conscientiousnessx, Extraversionx, Agreeablenessx, Neuroticismx),
	requester(NameRequester, _, Opennessy, Conscientiousnessy, Extraversiony, Agreeablenessy, Neuroticismy),
	\+ (inRange(0.0329318, 0.4329318 ,Conscientiousnessx)),
	\+ (inRange(0.26503104, 0.46503104 ,Conscientiousnessy)),
	format("Closer: ~w and Requester: ~w might work well!", [NameCloser,NameRequester]).

might_work_well(NameCloser, NameRequester) :-
	closer(NameCloser, _, Opennessx, Conscientiousnessx, Extraversionx, Agreeablenessx, Neuroticismx),
	requester(NameRequester, _, Opennessy, Conscientiousnessy, Extraversiony, Agreeablenessy, Neuroticismy),
	inRange(0.00763253, 0.10763253 ,Extraversionx),
	inRange(0.22890639, 0.32890639 ,Extraversiony),
	format("Closer: ~w and Requester: ~w might work well!", [NameCloser,NameRequester]).

might_work_well(NameCloser, NameRequester) :-
	closer(NameCloser, _, Opennessx, Conscientiousnessx, Extraversionx, Agreeablenessx, Neuroticismx),
	requester(NameRequester, _, Opennessy, Conscientiousnessy, Extraversiony, Agreeablenessy, Neuroticismy),
	inRange(0.04156959, 0.00156959 ,Agreeablenessx),
	inRange(0.37773928, 0.33773928 ,Agreeablenessy),
	format("Closer: ~w and Requester: ~w might work well!", [NameCloser,NameRequester]).
	