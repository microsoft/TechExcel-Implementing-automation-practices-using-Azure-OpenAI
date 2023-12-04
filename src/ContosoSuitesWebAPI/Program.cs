var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.MapGet("/Customer", (string searchCriterion, string searchValue) => 
{
    // TODO: implement search.
    // TODO: Replace with a call to Cosmos DB.
    var customer = new Customer
    {
        FirstName = "John",
        LastName = "Doe",
        FullName = "John Doe",
        LoyaltyTier = LoyaltyTier.Gold,
        YearsAsMember = 2,
        DateOfMostRecentStay = DateTime.Now.AddDays(-1),
        AverageRating = 4.5
    };
    return customer;
})
    .WithName("GetCustomer")
    .WithOpenApi();

app.Run();
